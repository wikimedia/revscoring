from nose.tools import eq_

from ..threshold_optimization import ThresholdOptimization


def test_threshold_optimization():
    ThresholdOptimization.parse("maximum precision @ recall >= 0.9")
    to = ThresholdOptimization.parse("maximum precision @ !recall >= 0.9")
    eq_(to.maximize, True)
    eq_(to.target_stat, "precision")
    eq_(to.cond_stat, "!recall")
    eq_(to.greater, True)
    eq_(to.cond_value, 0.9)

    to = ThresholdOptimization.parse("minimum waffle_monster @ peet <= 0.001")
    eq_(to.maximize, False)
    eq_(to.target_stat, "waffle_monster")
    eq_(to.cond_stat, "peet")
    eq_(to.greater, False)
    eq_(to.cond_value, 0.001)
