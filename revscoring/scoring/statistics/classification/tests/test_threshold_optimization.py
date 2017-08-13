from ..threshold_optimization import ThresholdOptimization


def test_threshold_optimization():
    ThresholdOptimization.parse("maximum precision @ recall >= 0.9")
    to = ThresholdOptimization.parse("maximum precision @ !recall >= 0.9")
    assert to.cond_stat == "!recall"
