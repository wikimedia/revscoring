import pickle

from nose.tools import eq_

from ....datasources import revision_oriented
from ....dependencies import solve
from ..revision_oriented import revision

length_change = revision.parent.length - revision.length


def test_length():
    cache = {revision_oriented.revision.parent.text: "I am ascii",
             revision_oriented.revision.text: "地を南北に縦走する"}

    eq_(solve(revision.length, cache=cache), 27)
    eq_(solve(revision.parent.length, cache=cache), 10)
    eq_(solve(length_change, cache=cache), -17)

    eq_(pickle.loads(pickle.dumps(revision.length)), revision.length)
    eq_(pickle.loads(pickle.dumps(revision.parent.length)),
        revision.parent.length)
    eq_(pickle.loads(pickle.dumps(length_change)), length_change)
