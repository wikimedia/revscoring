import pickle

from revscoring.datasources import session_oriented
from revscoring.dependencies import solve
from revscoring.features.wikitext import session

r_text = session_oriented.session.revisions.text
p_text = session_oriented.session.revisions.parent.text


cite_templates_ds = session.revisions.datasources.template_names_matching(r"^cite")
cite_templates = session.revisions.template_names_matching(r"^cite")


def test_session_chars():
    cache = {p_text: ["This is some nice text.", ""],
             r_text: ["This is some more text.", "I have a hat."]}

    assert solve(session.revisions.chars, cache=cache) == [23, 13]
    assert solve(session.revisions.parent.chars, cache=cache) == [23, 0]
    assert solve(session.revisions.diff.chars_added, cache=cache) == [4, 13]
    assert solve(session.revisions.diff.chars_removed, cache=cache) == [4, 0]

    assert (pickle.loads(pickle.dumps(session.revisions.chars)) ==
            session.revisions.chars)
    assert (pickle.loads(pickle.dumps(session.revisions.parent.chars)) ==
            session.revisions.parent.chars)
    assert (pickle.loads(pickle.dumps(session.revisions.diff.chars_added)) ==
            session.revisions.diff.chars_added)
    assert (pickle.loads(pickle.dumps(session.revisions.diff.chars_removed)) ==
            session.revisions.diff.chars_removed)


def test_session_tokens_matching():
    cache = {p_text: ["This is not 55 a sring.", ""],
             r_text: ["This is too 56 a tring.", "Foobar!"]}
    assert (solve(session.revisions.diff.datasources.tokens_added_matching("^t"),
                  cache=cache) ==
            [['too', 'tring'], []])
    assert (solve(session.revisions.diff.datasources.tokens_removed_matching("^(5|s)"),
                  cache=cache) ==
            [['55', 'sring'], []])


def test_templates():

    cache = {r_text: ["This is [https://wikis.com].\n" +
                      "== Heading! ==\n" +
                      "<ref>{{Cite thing}}</ref> the {{citation needed}}\n" +
                      "=== Another {{heading|foo}}! ===", ""]}
    assert (solve(session.revisions.datasources.template_names, cache=cache) ==
            [["Cite thing", "citation needed", "heading"], []])

    assert solve(session.revisions.templates, cache=cache) == [3, 0]

    assert solve(cite_templates, cache=cache) == [1, 0]

    assert (pickle.loads(pickle.dumps(session.revisions.templates)) ==
            session.revisions.templates)
    assert (pickle.loads(pickle.dumps(cite_templates)) ==
            cite_templates)


def test_tokens():
    text = """
This is an m80.  It has 50 grams of TNT. Here's some japanese:
修造のための勧進を担った組織の総称。[//google.com?foo=bar hats]
I can use &middot; and &nbsp;.  But [[can]] I {{foo}} a {{bar}}?

I guess we'll never know.
"""
    assert solve(session.revisions.tokens, cache={r_text: [text, ""]}) == [97, 0]
    assert pickle.loads(pickle.dumps(session.revisions.tokens)) == session.revisions.tokens

    my_words = session.revisions.datasources.tokens_in_types({"word"})
    assert (solve(my_words, cache={r_text: [text, ""]}) ==
            [['This', 'is', 'an', 'm80', 'It', 'has', 'grams', 'of', 'TNT',
              "Here's", 'some', 'japanese', 'hats', 'I', 'can', 'use', 'and',
              'But', 'can', 'I', 'foo', 'a', 'bar', 'I', 'guess', "we'll", 'never',
              'know'], []])
    assert pickle.loads(pickle.dumps(my_words)) == my_words
