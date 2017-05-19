import pickle

from nose.tools import eq_

from .. import revision
from ....datasources import revision_oriented
from ....dependencies import solve

h_headings_ds = revision.datasources.heading_titles_matching(r"h")
h_headings = revision.heading_titles_matching(r"h")
lvl_2_headings_ds = revision.datasources.headings_by_level(2)
lvl_2_headings = revision.headings_by_level(2)
enwiki_wikilinks_ds = revision.datasources.wikilink_titles_matching(r"^:?en:")
enwiki_wikilinks = revision.wikilink_titles_matching(r"^:?en:")
wikimedia_external_links_ds = \
    revision.datasources.external_link_urls_matching(r".*wikimedia.*")
wikimedia_external_links = \
    revision.external_link_urls_matching(r".*wikimedia.*")
cite_templates_ds = revision.datasources.template_names_matching(r"^cite")
cite_templates = revision.template_names_matching(r"^cite")

r_text = revision_oriented.revision.text


def test_content():

    cache = {r_text: "This is some text.\n" +
                      "== A heading! ==\n" +
                      "{{Foo}} the [[bar]]!"}
    eq_(solve(revision.datasources.content, cache=cache),
        "This is some text.\n" +
        " A heading! \n" +
        " the bar!")

    eq_(solve(revision.content_chars, cache=cache), 41)

    eq_(pickle.loads(pickle.dumps(revision.content_chars)),
        revision.content_chars)

    test_data = """
        Playing games has always been thought to be
        important to the development of well-balanced and creative children; however,
        what part, if any, they should play in the lives of adults has never been
        researched that deeply. I believe that playing games is every bit as important
        for adults as for children. Not only is taking time out to play games with our
        children and other adults valuable to building interpersonal relationships but
        is also a wonderful way to release built up tension."""
    cache = {r_text: test_data}
    eq_(solve(revision.flesh_kincaid, cache=cache), 52.23)
    eq_(pickle.loads(pickle.dumps(revision.flesh_kincaid)),
        revision.flesh_kincaid)

def test_headings():

    cache = {r_text: "This is some text.\n" +
                      "== Heading! ==\n" +
                      "{{Foo}} the [[bar]]!\n" +
                      "=== Another heading! ==="}
    eq_(solve(revision.datasources.heading_titles, cache=cache),
        ["Heading!", "Another heading!"])

    eq_(solve(revision.headings, cache=cache), 2)

    eq_(solve(h_headings, cache=cache), 1)

    eq_(solve(lvl_2_headings, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(revision.headings)), revision.headings)
    eq_(pickle.loads(pickle.dumps(h_headings)), h_headings)
    eq_(pickle.loads(pickle.dumps(lvl_2_headings)), lvl_2_headings)


def test_wikilinks():

    cache = {r_text: "This is [[:en:some|text]].\n" +
                      "== Heading! ==\n" +
                      "{{Foo}} the [[bar]]!\n" +
                      "=== Another heading! ==="}
    eq_(solve(revision.datasources.wikilink_titles, cache=cache),
        [":en:some", "bar"])

    eq_(solve(revision.wikilinks, cache=cache), 2)

    eq_(solve(enwiki_wikilinks, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(revision.wikilinks)), revision.wikilinks)
    eq_(pickle.loads(pickle.dumps(enwiki_wikilinks)), enwiki_wikilinks)


def test_external_links():

    cache = {r_text: "This is [https://wikis.com].\n" +
                      "== Heading! ==\n" +
                      "{{Foo}} the [//meta.wikimedia.org foobar]!\n" +
                      "=== Another heading! ==="}
    eq_(solve(revision.datasources.external_link_urls, cache=cache),
        ["https://wikis.com", "//meta.wikimedia.org"])

    eq_(solve(revision.external_links, cache=cache), 2)

    eq_(solve(wikimedia_external_links, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(revision.external_links)),
        revision.external_links)
    eq_(pickle.loads(pickle.dumps(wikimedia_external_links)),
        wikimedia_external_links)


def test_tags():

    cache = {r_text: "This is [https://wikis.com].\n" +
                      "== Heading! ==\n" +
                      "<ref>Foo</ref> the <span>foobar</span>!\n" +
                      "=== Another heading! ==="}
    eq_(solve(revision.datasources.tag_names, cache=cache),
        ["ref", "span"])

    eq_(solve(revision.tags, cache=cache), 2)

    eq_(solve(revision.ref_tags, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(revision.tags)),
        revision.tags)
    eq_(pickle.loads(pickle.dumps(revision.ref_tags)),
        revision.ref_tags)


def test_templates():

    cache = {r_text: "This is [https://wikis.com].\n" +
                      "== Heading! ==\n" +
                      "<ref>{{Cite thing}}</ref> the {{citation needed}}\n" +
                      "=== Another {{heading|foo}}! ==="}
    eq_(solve(revision.datasources.template_names, cache=cache),
        ["Cite thing", "citation needed", "heading"])

    eq_(solve(revision.templates, cache=cache), 3)

    eq_(solve(cite_templates, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(revision.templates)),
        revision.templates)
    eq_(pickle.loads(pickle.dumps(cite_templates)),
        cite_templates)
