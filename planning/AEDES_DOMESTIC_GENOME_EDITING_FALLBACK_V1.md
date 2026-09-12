# Aedes domestic genome-editing fallback v1

## Status

Logistics/fallback planning only. This file is downstream of `freeze/aedes-execution-readiness-v1`. It does not authorize line reconstruction now and does not modify the frozen scientific task or execution gates.

## Executive conclusion

If live `Ir68a^EYFP` / `Ir68a^RFP` import or transfer becomes the decisive logistics bottleneck, a **domestic reconstruction route is technically plausible**, but public evidence does not support assigning that capability to one Japanese institution alone.

The strongest current domestic capability map is:

- **Jikei University School of Medicine** — clear live-mosquito / medical-entomology infrastructure and current Aedes research;
- **Kyoto University Daimon group** — clear DIPA-CRISPR method-development expertise and coauthorship on the 2023 Aedes DIPA-CRISPR demonstration;
- the 2023 Aedes DIPA paper was a Kyoto–Jikei collaboration.

Publicly accessible sources do not establish with sufficient confidence whether the live *Aedes aegypti* colony and adult injections in that study were physically performed at Kyoto or Jikei. Therefore the fallback should be described as a **Kyoto–Jikei collaborative capability**, not “Kyoto already has an Aedes editing facility.”

## 1. Jikei capability

Jikei currently maintains a specialized medical-entomology platform:

- Tropical Medicine / Medical Entomology research centered on mosquito/vector biology;
- Center for Medical Entomology described by Jikei as a unique university platform in Japan for medically important arthropods;
- current Aedes feeding/vector studies;
- Hirotaka Kanuka and Manabu Ote were coauthors on the 2023 Aedes DIPA-CRISPR paper.

This is strong evidence for mosquito handling/infrastructure, but does not by itself prove current capacity for the exact Ir68a knock-in procedure.

## 2. Kyoto capability

Takaaki Daimon / Kyoto University developed DIPA-CRISPR and remains an active insect gene-editing group.

The Kyoto group:

- established DIPA-CRISPR as an adult-injection gene-editing method;
- coauthored the 2023 successful Aedes DIPA-CRISPR application;
- continues to apply direct-parental CRISPR in other insects;
- publicly provides the lead-contact route for DIPA method/reagent questions.

Public contact:

- Takaaki Daimon — `daimon.takaaki.7a@kyoto-u.ac.jp`

The current evidence supports **method expertise**, not a claim that Kyoto independently maintains a live Aedes colony today.

## 3. Why DIPA is relevant but not an immediate substitute for Tang knock-ins

The published Aedes DIPA study recovered edited G0 individuals after adult female Cas9-RNP injection, with the best reported editing efficiency when females were injected 24 h after blood feeding.

This is valuable because it can simplify generation of loss-of-function alleles without embryo injection.

However, the frozen Phase 2 causal asset is not merely an `Ir68a` loss-of-function:

- Tang et al. used two independent tagged knock-in alleles (`Ir68a^EYFP`, `Ir68a^RFP`);
- the tagged alleles support precise causal/reporter interpretation;
- recreating the same HDR/knock-in architecture is more demanding than producing a simple NHEJ knockout.

Therefore DIPA-CRISPR should not be treated as a drop-in way to recreate the exact Tang lines without method development.

## 4. Fallback hierarchy

### F0 — preferred

Obtain the published `Ir68a^EYFP` and `Ir68a^RFP` lines directly from Garrity.

### F1 — if live-line transfer is blocked but DNA/reagents can move

Ask Garrity for:

- exact donor plasmids;
- gRNA/Cas9 plasmids or sequences;
- guide sequences;
- homology-arm coordinates/sequences;
- genotype verification primers;
- any unpublished strain-construction notes.

Then evaluate domestic reconstruction on the exact comparator background.

### F2 — domestic editing feasibility study

Before attempting Ir68a reconstruction, ask the Kyoto–Jikei collaborators whether:

1. adult DIPA can support the required HDR/tagged knock-in architecture in Aedes, or only efficient mutagenesis;
2. conventional Aedes embryo injection is available domestically for precise knock-in if DIPA is inadequate;
3. a Liverpool/LVP-IB12 colony can be used at the editing facility;
4. the work can be performed under the facility's current containment/compliance framework.

### F3 — simple loss-of-function substitute

Do **not** replace the two tagged Tang alleles with newly generated simple knockouts merely because they are easier to make.

A simple knockout may become a new prospectively defined validation route, but it cannot inherit the frozen Phase 2 two-allele qualification automatically.

## 5. Specific domestic contacts to clarify capability

### Jikei

Hirotaka Kanuka / Tropical Medicine and Medical Entomology
Public institutional contact: `kanuka@jikei.ac.jp`

Question:
> In the 2023 Aedes DIPA-CRISPR collaboration, where were the live Aedes colonies and adult injections performed, and does Jikei currently have capacity to generate/rear edited Aedes lines for an academic collaboration?

### Kyoto

Takaaki Daimon
`daimon.takaaki.7a@kyoto-u.ac.jp`

Question:
> For Aedes, is your current DIPA-CRISPR workflow suitable only for mutagenesis, or is precise donor-mediated knock-in feasible enough to recreate tagged Ir68a alleles? If live Aedes work is not performed in Kyoto, which collaborating facility currently supports the mosquito component?

## 6. Decision rules

### If Jikei/Kyoto can recreate tagged alleles on the exact comparator background

Domestic reconstruction becomes a viable backup **only after** direct line transfer has failed or become impractical.

### If only simple DIPA knockout is practical

Keep the Tang tagged-line route as primary. A simple knockout design requires a new prospective Phase 2 validation specification.

### If no domestic precise-editing route exists

Return to live-line transfer/import planning; do not weaken the allele requirement post hoc.

## 7. Hard stops

- do not infer the physical site of the 2023 Aedes DIPA experiments from author affiliation alone;
- do not equate DIPA mutagenesis with precise HDR knock-in capability;
- do not replace the published two-allele package because a simpler domestic edit is convenient;
- do not begin line reconstruction before pedigree compatibility and receiving facility are fixed;
- do not use edited-line feasibility as evidence for the adaptive-gain hypothesis.

## Evidence anchors

- Shirai et al. 2023, Applied Entomology and Zoology: successful DIPA-CRISPR in Aedes; Kyoto and Jikei coauthors.
- Jikei Medical Entomology / Tropical Medicine: current specialized vector/arthropod research platform.
- Daimon lab, Kyoto University: DIPA-CRISPR method-development and continued insect editing work.
- Tang et al. 2024 PNAS: exact Ir68a tagged knock-in construct classes and unrestricted generated-reagent request path.
