import pickle

from deltas import Delete, Equal, Insert
from nose.tools import eq_

from ......datasources import parent_revision, revision
from ......dependencies import solve
from ..segments import segments_added, segments_removed


def test_segments():
    cache = {parent_revision.text: "This is not a string.",
             revision.text: "This is too a int!"}
    eq_(solve(segments_added, cache=cache),
        ['too', 'int!'])
    eq_(solve(segments_removed, cache=cache),
        ['not', 'string.'])

    eq_(pickle.loads(pickle.dumps(segments_added)), segments_added)
    eq_(pickle.loads(pickle.dumps(segments_removed)), segments_removed)
