from nose.tools import eq_, raises

from .. import revision
from ...dependencies import solve
from ...errors import RevisionNotFound


def test_content():
    cache = {revision.text: "This is some {{markup}} and [[stuff]]."}
    content = solve(revision.content, cache=cache)
    eq_(content, "This is some  and stuff.")

    cache = {revision.text: "This is a foobar {{foobar}} <td>"}
    eq_(solve(revision.content_tokens, cache=cache),
        ["This", " ", "is", " ", "a", " ", "foobar", "  "])


def test_headings():
    text = """
= Heading 1 =
Foo bar baz.

== Heading 2 ==
Doo be doo be doo? ==Hats==

== Heading 2 again ==
Testing some text.

====== HEADING 6 ======
    """
    headings = solve(revision.headings, cache={revision.text: text})

    eq_([h.level for h in headings], [1, 2, 2, 6])


def test_intental_links():
    text = "This is some [[Text]] with [http://foobar] [[links|hyperlinks]]"

    internal_links = solve(revision.internal_links,
                           cache={revision.text: text})

    eq_([str(l.title) for l in internal_links], ["Text", "links"])


def test_tags():
    text = "This <span>is</span> <ref>tags</ref> to <!--<ref>detect</ref>-->"

    tags = solve(revision.tags, cache={revision.text: text})

    eq_([str(t.tag) for t in tags], ["span", "ref"])


def test_templates():
    text = """
{{template0}}
= Heading 1 {{template1}}=
Foo bar baz.

== Heading 2 ==

== Heading 2 again ==
Testing some text. {{:User:Hats/Template3}}

====== HEADING 6 ======
    """
    templates = solve(revision.templates, cache={revision.text: text})

    eq_([str(t.name) for t in templates], ["template0", "template1",
                                           ":User:Hats/Template3"])


@raises(RevisionNotFound)
def test_not_found_tokens():
    solve(revision.tokens, cache={revision.text: None})


@raises(RevisionNotFound)
def test_not_found_parse_tree():
    solve(revision.parse_tree, cache={revision.text: None})
