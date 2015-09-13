from nose.tools import eq_

from .. import parent_revision
from ...dependencies import solve


def test_tokens():
    cache = {parent_revision.text: "Some text words 55."}
    eq_(solve(parent_revision.tokens, cache=cache),
        ["Some", " ", "text", " ", "words", " ", "55", "."])

    # Make sure we don't error when there is no parent revision
    cache = {parent_revision.text: None}
    eq_(solve(parent_revision.tokens, cache=cache),
        [])


def test_content():
    cache = {parent_revision.text: "Some text words 55. {{foo}}"}
    eq_(solve(parent_revision.content, cache=cache),
        "Some text words 55. ")

    # Make sure we don't error when there is no parent revision
    cache = {parent_revision.text: None}
    eq_(solve(parent_revision.content, cache=cache), "")

    cache = {parent_revision.text: "This is a foobar {{foobar}} <td>"}
    eq_(solve(parent_revision.content_tokens, cache=cache),
        ["This", " ", "is", " ", "a", " ", "foobar", "  "])
