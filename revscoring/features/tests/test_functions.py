from nose.tools import eq_

from ...datasources import Datasource
from ..feature import Feature
from ..functions import trim
from ..modifiers import log, max


def test_trim():

    d1 = Datasource("derp1")
    f1 = Feature("foobar1", returns=int)
    f2 = Feature("foobar2", returns=int, depends_on=[d1])

    eq_(list(trim(f1)), [f1])
    eq_(list(trim([f1, f2])), [f1, f2])
    eq_(list(trim(log(max(f1 - f2, 1)))),
        [f1, f2])
