
from revscoring.scoring.statistics.classification.threshold_optimization import \
    ThresholdOptimization


def test_threshold_optimization():
    ThresholdOptimization.parse("maximum precision @ recall >= 0.9")
    to = ThresholdOptimization.parse("maximum precision @ !recall >= 0.9")
    assert to.maximize is True
    assert to.target_stat == "precision"
    assert to.cond_stat == "!recall"
    assert to.greater is True
    assert to.cond_value == 0.9

    to = ThresholdOptimization.parse("minimum waffle_monster @ peet <= 0.001")
    assert to.maximize is False
    assert to.target_stat == "waffle_monster"
    assert to.cond_stat == "peet"
    assert to.greater is False
    assert to.cond_value == 0.001
