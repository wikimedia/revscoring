from nose.tools import eq_, raises

from .. import parent_revision
from ....dependencies import solve
from ....errors import RevisionNotFound
from ...parent_revision import text as parent_revision_text


def test_tokens_types():
    text = "This is 34.\n\nM80s are cool? し{{foo}}[//google.com]\t&nbsp;"
    cache = {parent_revision_text: text}
    eq_(solve(parent_revision.number_tokens, cache=cache), ['34'])
    eq_(solve(parent_revision.whitespace_tokens, cache=cache),
        [' ', ' ', ' ', ' ', ' ', '\t'])
    eq_(solve(parent_revision.markup_tokens, cache=cache),
        ['{{', '}}', '[', ']'])
    eq_(solve(parent_revision.cjk_tokens, cache=cache), ['し'])
    eq_(solve(parent_revision.entity_tokens, cache=cache), ['&nbsp;'])
    eq_(solve(parent_revision.url_tokens, cache=cache), ['//google.com'])
    eq_(solve(parent_revision.word_tokens, cache=cache),
        ['This', 'is', 'M80s', 'are', 'cool', 'foo'])
    eq_(solve(parent_revision.punctuation_tokens, cache=cache), ['.', '?'])
    eq_(solve(parent_revision.break_tokens, cache=cache), ['\n\n'])


def test_content():
    cache = {parent_revision_text: "This is some {{markup}} and [[stuff]]."}
    content = solve(parent_revision.content, cache=cache)
    eq_(content, "This is some  and stuff.")

    cache = {parent_revision_text: "This is a foobar {{foobar}} <td>"}
    eq_(solve(parent_revision.content_tokens, cache=cache),
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
    headings = solve(parent_revision.headings,
                     cache={parent_revision_text: text})

    eq_([h.level for h in headings], [1, 2, 2, 6])

    eq_(solve(parent_revision.heading_titles,
              cache={parent_revision_text: text}),
        ["Heading 1", "Heading 2", "Heading 2 again", "HEADING 6"])


def test_intental_link_titles():
    text = "This is some [[Text]] with [http://foobar] [[links|hyperlinks]]"

    eq_(solve(parent_revision.internal_link_titles,
              cache={parent_revision_text: text}),
        ["Text", "links"])


def test_external_link_urls():
    text = "This is some [http://foobar] with [//foobar] [[links|hyperlinks]]"

    eq_(solve(parent_revision.external_link_urls,
              cache={parent_revision_text: text}),
        ["http://foobar", "//foobar"])


def test_tag_names():
    text = "This <span>is</span> <ref>tags</ref> to <!--<ref>detect</ref>-->"

    eq_(solve(parent_revision.tag_names, cache={parent_revision_text: text}),
        ["span", "ref"])


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
    eq_(solve(parent_revision.template_names,
              cache={parent_revision_text: text}),
        ["template0", "template1", ":User:Hats/Template3"])


def test_not_found_tokens():
    solve(parent_revision.tokens, cache={parent_revision_text: None})


def test_not_found_parse_tree():
    solve(parent_revision.parse_tree, cache={parent_revision_text: None})
