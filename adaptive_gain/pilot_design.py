"""Reproducible *pre-exposure* bee-blocked pilot allocation and cue schedules.

The generator cannot conduct randomization in animals, secure blindness, prove
external time-locking of a plan, validate apparatus delivery or infer fitness.
Keep the private 256-bit seed outside shared repository files. All generated
CSV files are *plans*, never records of observed bee behavior.

The fixed-arm second cue, target identity and A-context stimulus are balanced
within each bee using an eight-cell factorial schedule. For a real pilot this
requires a prospective multiple-of-eight trial count per bee, NOT a recommended
sample size or power calculation. Animal-colony interference must be assessed
separately before any bee-level randomized inference.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
import hashlib
import hmac
import io
import json
import os
from pathlib import Path
import re
import secrets
from collections import Counter, defaultdict
from typing import Sequence

from .pilot_itt import PilotBee, PilotTrial
from .pilot_process import FixedCuePlan

_SCHEMA = "bee_randomized_pilot_design_v1"
_LOCKED_FILES = ("bee_roster.csv", "stimulus_schedule.csv", "bee_fixed_plans.csv")
_HEX_256 = re.compile(r"[0-9A-Fa-f]{64}\Z")
_LAB_ID = re.compile(r"[a-zA-Z0-9_.-]+\Z")


@dataclass(frozen=True)
class BeeInventory:
    bee_id: str
    colony_id: str


@dataclass(frozen=True)
class StimulusSlot:
    trial_id: str
    bee_id: str
    slot: int
    target: int
    context_truth: int
    first_cue: str = "A"


@dataclass(frozen=True)
class PilotDesign:
    roster: tuple[PilotBee, ...]
    presentations: tuple[StimulusSlot, ...]
    fixed_plans: tuple[FixedCuePlan, ...]
    trial_template: tuple[PilotTrial, ...]
    slots_per_bee: int
    seed_commitment: str
    plan_archive_id: str


class _SeededShuffle:
    """Domain-separated HMAC-SHA256 shuffle with rejection-sampled indices.

    Within supported small enrollment sizes, a uniform Fisher-Yates shuffle
    on independent pseudorandom HMAC outputs avoids modulo-selection bias.
    This does not establish an externally verifiable randomization timestamp.
    """

    def __init__(self, seed: bytes, domain: str) -> None:
        self.key = hmac.new(seed, domain.encode("utf-8"), hashlib.sha256).digest()
        self.counter = 0

    def randbelow(self, n: int) -> int:
        if n < 1 or n >= (1 << 256):
            raise ValueError("invalid random selection range")
        limit = (1 << 256) - ((1 << 256) % n)
        while True:
            message = self.counter.to_bytes(16, "big")
            self.counter += 1
            draw = int.from_bytes(hmac.new(self.key, message, hashlib.sha256).digest(), "big")
            if draw < limit:
                return draw % n

    def shuffle(self, values):
        items = list(values)
        for i in range(len(items) - 1, 0, -1):
            j = self.randbelow(i + 1)
            items[i], items[j] = items[j], items[i]
        return items


def _seed_from_hex(seed_hex: str) -> bytes:
    if not isinstance(seed_hex, str) or not _HEX_256.fullmatch(seed_hex):
        raise ValueError("seed must be exactly 64 hexadecimal characters (256 bits)")
    return bytes.fromhex(seed_hex)


def _stimulus_schedule_for_bee(bee_id: str, seed_hex: str, *, slots_per_bee: int):
    """World/context balance independent of the bee's treatment assignment."""
    seed = _seed_from_hex(seed_hex)
    if type(slots_per_bee) is not int or slots_per_bee < 8 or slots_per_bee % 8:
        raise ValueError("slots_per_bee must be a positive multiple of eight")
    pairs = [(target, context) for target in (0, 1) for context in (0, 1)
             for _ in range(slots_per_bee // 4)]
    return _SeededShuffle(seed, "v1|stimulus|" + bee_id).shuffle(pairs)


def design_pilot(
    inventory: Sequence[BeeInventory], *, slots_per_bee: int, seed_hex: str,
) -> PilotDesign:
    """Generate the pre-outcome blocked allocation and balanced cue schedule.

    Allocation is equal within each colony, including a minimum two bees in
    each arm; colonies with fewer than four or an odd count are rejected.
    Stimulus (target, context) sequences are generated without looking at the
    assigned treatment, so their distributions are fixed under arm reassignment.
    Fixed controls receive both B and C exactly once per target/context cell
    per eight slots, from a separate domain of the private seed.
    """
    seed = _seed_from_hex(seed_hex)
    if type(slots_per_bee) is not int or slots_per_bee < 8 or slots_per_bee % 8:
        raise ValueError("slots_per_bee must be a positive multiple of eight")
    rows = tuple(inventory)
    if not rows:
        raise ValueError("pre-enrollment inventory is required")
    seen = set()
    colonies = defaultdict(list)
    for bee in rows:
        if not isinstance(bee, BeeInventory) or any(
            not isinstance(v, str) or not _LAB_ID.fullmatch(v)
            for v in (bee.bee_id, bee.colony_id)
        ):
            raise ValueError("bee_id and colony_id must use nonempty ASCII letters/digits/underscore/dot/hyphen")
        if bee.bee_id in seen:
            raise ValueError("duplicate bee_id across inventory")
        seen.add(bee.bee_id)
        colonies[bee.colony_id].append(bee.bee_id)
    if any(len(ids) < 4 or len(ids) % 2 for ids in colonies.values()):
        raise ValueError("every colony requires an even number >= 4 of enrolled bees")

    assignment = {}
    for colony in sorted(colonies):
        ids = sorted(colonies[colony])
        chosen = _SeededShuffle(seed, "v1|allocation|" + colony).shuffle(ids)
        contingent = set(chosen[: len(ids)//2])
        for bee in ids:
            assignment[bee] = "contingent" if bee in contingent else "precommitted"

    roster = []
    presentations = []
    fixed_plans = []
    templates = []
    commitment = hashlib.sha256(seed).hexdigest()
    archive_id = "preexposure-" + commitment[:16]
    for colony in sorted(colonies):
        for bee in sorted(colonies[colony]):
            arm = assignment[bee]
            roster.append(PilotBee(bee, colony, arm))
            stimulus_sequence = _stimulus_schedule_for_bee(
                bee, seed_hex, slots_per_bee=slots_per_bee
            )
            fixed_bags = {}
            if arm == "precommitted":
                for target in (0, 1):
                    for context in (0, 1):
                        bag = ["B"] * (slots_per_bee // 8) + ["C"] * (slots_per_bee // 8)
                        fixed_bags[(target, context)] = iter(
                            _SeededShuffle(seed, f"v1|fixed|{bee}|{target}|{context}").shuffle(bag)
                        )
            for slot, (target, context) in enumerate(stimulus_sequence, 1):
                trial_id = f"{bee}__slot{slot:04d}"
                presentations.append(StimulusSlot(trial_id, bee, slot, target, context))
                templates.append(PilotTrial(trial_id, bee, slot, target,
                                            "unobserved", None, "not_yet_run", ""))
                if arm == "precommitted":
                    fixed_plans.append(FixedCuePlan(
                        trial_id, bee, next(fixed_bags[(target, context)]), archive_id
                    ))
    return PilotDesign(tuple(roster), tuple(presentations), tuple(fixed_plans),
                       tuple(templates), slots_per_bee, commitment, archive_id)


def _csv_bytes(headers, rows) -> bytes:
    io_text = io.StringIO(newline="")
    w = csv.writer(io_text, lineterminator="\n")
    w.writerow(headers)
    w.writerows(rows)
    return io_text.getvalue().encode("utf-8")


def _manifest(design: PilotDesign, locked_files: dict[str, bytes]) -> dict:
    colony_counts = {}
    for b in design.roster:
        if b.colony_id not in colony_counts:
            colony_counts[b.colony_id] = {"contingent": 0, "precommitted": 0}
        colony_counts[b.colony_id][b.assigned_access] += 1
    return {
        "schema": _SCHEMA,
        "generator_version": 1,
        "seed_sha256_commitment": design.seed_commitment,
        "secret_seed_in_manifest": False,
        "plan_archive_id": design.plan_archive_id,
        "bees": len(design.roster),
        "colonies": len(colony_counts),
        "colony_assignments": colony_counts,
        "slots_per_bee": design.slots_per_bee,
        "slot_count": len(design.presentations),
        "fixed_plan_rows": len(design.fixed_plans),
        "actual_field_observations": False,
        "context_truth_is_not_perceived_A_report": True,
        "independent_external_time_lock_required": True,
        "locked_csv_sha256": {
            name: hashlib.sha256(locked_files[name]).hexdigest() for name in sorted(locked_files)
        },
    }


def render_pilot_design(design: PilotDesign) -> dict[str, bytes]:
    """Exact UTF-8 bytes for a sealed design plus a *mutable* unrun template."""
    locked = {
        "bee_roster.csv": _csv_bytes(
            ("bee_id", "colony_id", "assigned_access"),
            ((b.bee_id, b.colony_id, b.assigned_access) for b in design.roster),
        ),
        "stimulus_schedule.csv": _csv_bytes(
            ("trial_id", "bee_id", "slot", "target", "context_truth", "first_cue"),
            ((p.trial_id, p.bee_id, p.slot, p.target, p.context_truth, p.first_cue)
             for p in design.presentations),
        ),
        "bee_fixed_plans.csv": _csv_bytes(
            ("trial_id", "bee_id", "second_cue", "plan_archive_id"),
            ((p.trial_id, p.bee_id, p.second_cue, p.plan_archive_id)
             for p in design.fixed_plans),
        ),
    }
    receipt = _manifest(design, locked)
    files = {**locked,
             "design_manifest.json": (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2)
                                      + "\n").encode("utf-8"),
             "bee_trials_template.csv": _csv_bytes(
                 ("trial_id", "bee_id", "slot", "target", "outcome_status", "final_action",
                  "unobserved_reason", "delivered_access"),
                 ((t.trial_id, t.bee_id, t.slot, t.target, t.outcome_status,
                   "" if t.final_action is None else t.final_action,
                   t.unobserved_reason, t.delivered_access) for t in design.trial_template),
             )}
    return files


def _receipt(design: PilotDesign) -> dict:
    files = render_pilot_design(design)
    metadata = json.loads(files["design_manifest.json"])
    return {**metadata, "verified": True,
            "meaning_of_verified": "byte match to deterministic design; not proof of preregistration time"}


def write_pilot_design(design: PilotDesign, outdir: str | Path) -> dict:
    """Create a new output directory; never overwrite a prior sealed plan."""
    dest = Path(outdir)
    if dest.exists():
        raise FileExistsError("refusing to overwrite existing output directory")
    dest.mkdir(parents=True, exist_ok=False)
    for name, payload in render_pilot_design(design).items():
        (dest / name).write_bytes(payload)
    return _receipt(design)


def verify_pilot_design(design: PilotDesign, outdir: str | Path) -> dict:
    """Compare locked bytes to recomputation from private seed and inventory.

    The unrun trial template is deliberately excluded from the integrity gate:
    copy it before data entry and retain the locked schedules unchanged.
    """
    dest = Path(outdir)
    expected = render_pilot_design(design)
    for name in _LOCKED_FILES:
        if not (dest / name).is_file() or (dest / name).read_bytes() != expected[name]:
            raise ValueError(f"locked file mismatch: {name}")
    manifest = dest / "design_manifest.json"
    if not manifest.is_file() or manifest.read_bytes() != expected["design_manifest.json"]:
        raise ValueError("manifest mismatch")
    return _receipt(design)


def read_inventory_csv(path: str | Path) -> tuple[BeeInventory, ...]:
    with Path(path).open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not {"bee_id", "colony_id"}.issubset(reader.fieldnames):
            raise ValueError("inventory CSV requires bee_id,colony_id")
        return tuple(BeeInventory(row["bee_id"], row["colony_id"]) for row in reader)


def read_seed_hex(path: str | Path) -> str:
    return Path(path).read_text(encoding="ascii").strip()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Prepare / verify bee-blocked artificial-flower pilot allocations")
    commands = parser.add_subparsers(dest="command", required=True)
    seed = commands.add_parser("new-seed", help="create private entropy file, never commit it")
    seed.add_argument("--out", required=True)
    for command in ("generate", "verify"):
        sub = commands.add_parser(command)
        sub.add_argument("--inventory", required=True)
        sub.add_argument("--seed-file", required=True)
        sub.add_argument("--slots-per-bee", type=int, required=True)
        sub.add_argument("--outdir", required=True)
    args = parser.parse_args(argv)
    if args.command == "new-seed":
        filename = Path(args.out)
        filename.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="ascii") as handle:
            handle.write(secrets.token_hex(32) + "\n")
        print(json.dumps({"seed_path": str(filename), "private_seed_written": True,
                          "warning": "Do not upload this secret seed to GitHub"}))
        return
    design = design_pilot(
        read_inventory_csv(args.inventory), slots_per_bee=args.slots_per_bee,
        seed_hex=read_seed_hex(args.seed_file),
    )
    receipt = (write_pilot_design(design, args.outdir) if args.command == "generate"
               else verify_pilot_design(design, args.outdir))
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
