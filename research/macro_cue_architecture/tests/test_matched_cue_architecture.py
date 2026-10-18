"""Independent Fraction witness; not a claim of new general sequential-decision priority."""
import sys
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from verify_matched_cues import TASKS,TARGET,table,encode,dp_access,brute_access,fixed_access,result


def test_focal_pair_has_identical_single_cue_target_tables_and_no_duplicate_states():
    x,y=TASKS.values()
    assert len(set(encode(x)))==len(set(encode(y)))==6
    assert tuple(table(q) for q in x)==tuple(table(q) for q in y)
    assert len(set(TARGET))==2


def test_adaptive_premium_is_windowed_not_unconditional():
    for kind in ('guess','cert'):
        for budget in range(4):
            for matrix in TASKS.values():
                assert dp_access(matrix,budget,kind)==brute_access(matrix,budget,kind)
        assert dp_access(TASKS['nonrouteable'],2,kind)==fixed_access(TASKS['nonrouteable'],2,kind)
    assert dp_access(TASKS['routeable'],2,'guess')==1
    assert fixed_access(TASKS['routeable'],2,'guess')==Fraction(5,6)
    assert result['exhaustive_matched_family']['total']==135
