import pickle

from revscoring.datasources.session_oriented import session
from revscoring.dependencies import solve
from revscoring.features import bytes

length_change = \
    bytes.session.revisions.length - bytes.session.revisions.parent.length


def test_length():
    cache = {session.revisions.parent.text: ["I am ascii", "I am too"],
             session.revisions.text: ["地を南北に縦走する", ""]}

    assert solve(bytes.session.revisions.length, cache=cache) == [27, 0]
    assert solve(bytes.session.revisions.parent.length, cache=cache) == [10, 8]
    assert solve(length_change, cache=cache) == [17, -8]

    assert pickle.loads(pickle.dumps(bytes.session.revisions.length)) == \
           bytes.session.revisions.length
    assert (pickle.loads(pickle.dumps(bytes.session.revisions.parent.length)) ==
            bytes.session.revisions.parent.length)
    assert pickle.loads(pickle.dumps(length_change)) == length_change
