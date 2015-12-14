import pickle

from deltas import Delete, Equal, Insert
from nose.tools import eq_

from .. import diff, parent_revision, revision
from ....dependencies import solve

PARENT_REVISION_TEXT = "foo Bar 53 {{herp}} derp!"
REVISION_TEXT = "Herp Derp 75 {{and}} also?"
PARENT_REVISIONS_TOKENS = ['foo', ' ', 'Bar', ' ', '53', ' ', '{{', 'herp',
                           '}}', ' ', 'derp', '!']
REVISION_TOKENS = ['Herp', ' ', 'Derp', ' ', '75', ' ', '{{', 'and', '}}',
                   ' ', 'also', '?']

OPERATIONS = [Delete(a1=0, a2=1, b1=0, b2=0),  # "foo"
              Insert(a1=1, a2=1, b1=0, b2=1),  # "Herp"
              Equal(a1=1, a2=2, b1=1, b2=2),   # " "
              Delete(a1=2, a2=3, b1=2, b2=2),  # "Bar"
              Insert(a1=3, a2=3, b1=2, b2=3),  # "Derp"
              Equal(a1=3, a2=4, b1=3, b2=4),   # " "
              Delete(a1=4, a2=5, b1=4, b2=4),  # "53"
              Insert(a1=5, a2=5, b1=4, b2=5),  # "75"
              Equal(a1=5, a2=7, b1=5, b2=7),   # " {{"
              Delete(a1=7, a2=8, b1=7, b2=7),  # "herp"
              Insert(a1=8, a2=8, b1=7, b2=8),  # "and"
              Equal(a1=8, a2=10, b1=8, b2=10),  # "}} "
              Delete(a1=10, a2=12, b1=10, b2=10),  # "also?"
              Insert(a1=12, a2=12, b1=10, b2=12)]  # "derp!"


def test_operations():

    cache = {
        parent_revision.text: PARENT_REVISION_TEXT,
        revision.text: REVISION_TEXT
    }

    operations, a, b = solve(diff.operations, cache=cache)

    eq_(operations, OPERATIONS)

    eq_(a, PARENT_REVISIONS_TOKENS)

    eq_(b, REVISION_TOKENS)

    # Make sure we don't error when there is no parent revision
    cache = {
        parent_revision.text: None,
        revision.text: REVISION_TEXT
    }

    operations, a, b = solve(diff.operations, cache=cache)

    eq_(pickle.loads(pickle.dumps(diff.operations)), diff.operations)


def test_tokens_added():
    cache = {
        diff.operations: (OPERATIONS, PARENT_REVISIONS_TOKENS, REVISION_TOKENS)
    }

    tokens_added = solve(diff.tokens_added, cache=cache)

    eq_(tokens_added, ['Herp', 'Derp', '75', 'and', 'also', '?'])

    eq_(pickle.loads(pickle.dumps(diff.tokens_added)), diff.tokens_added)


def test_tokens_removed():
    cache = {
        diff.operations: (OPERATIONS, PARENT_REVISIONS_TOKENS, REVISION_TOKENS)
    }

    tokens_removed = solve(diff.tokens_removed, cache=cache)

    eq_(tokens_removed, ['foo', 'Bar', '53', 'herp', 'derp', '!'])

    eq_(pickle.loads(pickle.dumps(diff.tokens_removed)), diff.tokens_removed)


def test_segments_added():
    cache = {
        diff.operations: (OPERATIONS, PARENT_REVISIONS_TOKENS, REVISION_TOKENS)
    }

    segments_added = solve(diff.segments_added, cache=cache)

    eq_(segments_added, ['Herp', 'Derp', '75', 'and', 'also?'])

    eq_(pickle.loads(pickle.dumps(diff.segments_added)), diff.segments_added)


def test_segments_removed():
    cache = {
        diff.operations: (OPERATIONS, PARENT_REVISIONS_TOKENS, REVISION_TOKENS)
    }

    segments_removed = solve(diff.segments_removed, cache=cache)

    eq_(segments_removed, ['foo', 'Bar', '53', 'herp', 'derp!'])

    eq_(pickle.loads(pickle.dumps(diff.segments_removed)),
        diff.segments_removed)
