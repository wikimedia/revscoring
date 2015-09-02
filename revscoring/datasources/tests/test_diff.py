from deltas import Delete, Equal, Insert
from nose.tools import eq_

from .. import diff, parent_revision, revision
from ...dependencies import solve

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


def test_added_tokens():
    cache = {
        diff.operations: (OPERATIONS, PARENT_REVISIONS_TOKENS, REVISION_TOKENS)
    }

    added_tokens = solve(diff.added_tokens, cache=cache)

    eq_(added_tokens, ['Herp', 'Derp', '75', 'and', 'also', '?'])


def test_removed_tokens():
    cache = {
        diff.operations: (OPERATIONS, PARENT_REVISIONS_TOKENS, REVISION_TOKENS)
    }

    removed_tokens = solve(diff.removed_tokens, cache=cache)

    eq_(removed_tokens, ['foo', 'Bar', '53', 'herp', 'derp', '!'])


def test_added_segments():
    cache = {
        diff.operations: (OPERATIONS, PARENT_REVISIONS_TOKENS, REVISION_TOKENS)
    }

    added_segments = solve(diff.added_segments, cache=cache)

    eq_(added_segments, ['Herp', 'Derp', '75', 'and', 'also?'])


def test_removed_segments():
    cache = {
        diff.operations: (OPERATIONS, PARENT_REVISIONS_TOKENS, REVISION_TOKENS)
    }

    removed_segments = solve(diff.removed_segments, cache=cache)

    eq_(removed_segments, ['foo', 'Bar', '53', 'herp', 'derp!'])
