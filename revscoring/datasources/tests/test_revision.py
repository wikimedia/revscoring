from mw import Timestamp
from nose.tools import eq_

from .. import revision
from ...dependent import solve


def test_metadata():
    cache = {
        revision.doc: {
            "revid": 3456789,
            "parentid": 54678,
            "comment": "Wat?",
            "user": "EpochFail",
            "userid": 34567890,
            "timestamp": "2015-01-07T12:23:57Z",
            "page": {
                "pageid": 347,
                "title": "Hats",
                "ns": 0
            }
        }
    }

    metadata = solve(revision.metadata, cache=cache)

    eq_(metadata.rev_id, 3456789)
    eq_(metadata.parent_id, 54678)
    eq_(metadata.user_id, 34567890)
    eq_(metadata.user_text, "EpochFail")
    eq_(metadata.timestamp, Timestamp("2015-01-07T12:23:57Z"))
    eq_(metadata.comment,  "Wat?")
    eq_(metadata.page_id, 347)
    eq_(metadata.page_namespace, 0)
    eq_(metadata.page_title, "Hats")


def test_text():
    text = solve(revision.text,
                 cache={revision.doc: {"*": "Some text"}})
    eq_(text, "Some text")


def test_words():
    words = solve(revision.words,
                  cache={revision.text: "Some text words 55."})
    eq_(words, ["Some", "text", "words"])


def test_content():
    text = "This is some {{markup}} and [[stuff]]."

    content = solve(revision.content, cache={revision.text: text})

    eq_(content, "This is some  and stuff.")


def test_content_words():
    text = "This is some {{markup}} and [[stuff]]."

    content_words = solve(revision.content_words, cache={revision.text: text})

    eq_(content_words, ["This", "is", "some", "and", "stuff"])


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
