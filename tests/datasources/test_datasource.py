import pickle

from revscoring.datasources.datasource import Datasource
from revscoring.dependencies import solve


def test_datasource():

    d = Datasource("d")

    assert pickle.loads(pickle.dumps(d)) == d

    assert solve(d, cache={d: "foo"}) == "foo"

    assert solve(d, cache={"datasource.d": "foo"}) == "foo"

    assert str(d) == "datasource.d"
    assert repr(d) == "<datasource.d>"
