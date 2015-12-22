import pickle

from deltas import Delete, Equal, Insert
from nose.tools import eq_

from .. import segments
from ......datasources.revision_oriented import revision
from ......dependencies import solve


def test_segments():
    cache = {revision.parent.text: "This is not a string.",
             revision.text: "This is too a int!"}
    eq_(solve(segments.datasources.segments_added, cache=cache),
        ['too', 'int!'])
    eq_(solve(segments.segments_added, cache=cache), 2)
    eq_(solve(segments.datasources.segments_removed, cache=cache),
        ['not', 'string.'])
    eq_(solve(segments.segments_removed, cache=cache), 2)

    eq_(pickle.loads(pickle.dumps(segments.segments_added)),
        segments.segments_added)
    eq_(pickle.loads(pickle.dumps(segments.segments_removed)),
        segments.segments_removed)
