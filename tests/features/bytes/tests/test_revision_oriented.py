import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.features.bytes.revision_oriented import revision

length_change = revision.parent.length - revision.length


def test_length():
    cache = {revision_oriented.revision.parent.text: "I am ascii",
             revision_oriented.revision.text: "地を南北に縦走する"}

    assert solve(revision.length, cache=cache) == 27
    assert solve(revision.parent.length, cache=cache) == 10
    assert solve(length_change, cache=cache) == -17

    assert pickle.loads(pickle.dumps(revision.length)) == revision.length
    assert (pickle.loads(pickle.dumps(revision.parent.length)) ==
            revision.parent.length)
    assert pickle.loads(pickle.dumps(length_change)) == length_change
