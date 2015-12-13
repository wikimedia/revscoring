from nose.tools import eq_

from .. import parent_revision
from ....dependencies import solve
from ...parent_revision import text


def test_tokens():
    cache = {text: "Some text words 55."}
    eq_(solve(parent_revision.tokens, cache=cache),
        ["Some", " ", "text", " ", "words", " ", "55", "."])

    # Make sure we don't error when there is no parent revision
    cache = {text: None}
    eq_(solve(parent_revision.tokens, cache=cache),
        [])


def test_content():
    cache = {text: "Some text words 55. {{foo}}"}
    eq_(solve(parent_revision.content, cache=cache),
        "Some text words 55. ")

    # Make sure we don't error when there is no parent revision
    cache = {text: None}
    eq_(solve(parent_revision.content, cache=cache), "")

    cache = {text: "This is a foobar {{foobar}} <td>"}
    eq_(solve(parent_revision.content_tokens, cache=cache),
        ["This", " ", "is", " ", "a", " ", "foobar", "  "])
