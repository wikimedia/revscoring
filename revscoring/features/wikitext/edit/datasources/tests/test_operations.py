import pickle

from deltas import Delete, Equal, Insert
from nose.tools import eq_

from ......datasources import parent_revision, revision
from ......dependencies import solve
from ..operations import operations


def test_operations():
    cache = {parent_revision.text: "Foo Bar 53 {{herp}} derp!",
             revision.text: "Foo Bar 53 [[and]] derp!"}
    ops, a, b = solve(operations, cache=cache)

    eq_(ops, [Equal(a1=0, a2=6, b1=0, b2=6),
              Delete(a1=6, a2=9, b1=6, b2=6),
              Insert(a1=9, a2=9, b1=6, b2=9),
              Equal(a1=9, a2=12, b1=9, b2=12)])
    eq_(a, ['Foo', ' ', 'Bar', ' ', '53', ' ', '{{', 'herp', '}}', ' ',
            'derp', '!'])
    eq_(b, ['Foo', ' ', 'Bar', ' ', '53', ' ', '[[', 'and', ']]', ' ',
            'derp', '!'])

    eq_(pickle.loads(pickle.dumps(operations)), operations)
