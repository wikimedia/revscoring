import pickle

from nose.tools import eq_

from ......datasources import Datasource
from ......dependencies import solve
from .....meta import aggregators
from ..parsed_revision import ParsedRevision

my_text = Datasource("my_text")

my_parsed = ParsedRevision("my_text", my_text)

h_headings = aggregators.len(
    my_parsed.datasources.heading_titles_matching(r"h")
)
lvl_2_headings = aggregators.len(
    my_parsed.datasources.headings_by_level(2)
)
enwiki_wikilinks = aggregators.len(
    my_parsed.datasources.wikilink_titles_matching(r"^:?en:")
)
wikimedia_external_links = aggregators.len(
    my_parsed.datasources.external_link_urls_matching(r".*wikimedia.*")
)
ref_tags = aggregators.len(my_parsed.datasources.tag_names_matching(r"ref"))
cite_templates = aggregators.len(
    my_parsed.datasources.template_names_matching(r"^cite")
)


def test_content():

    cache = {my_text: "This is some text.\n" +
                      "== A heading! ==\n" +
                      "{{Foo}} the [[bar]]!"}
    eq_(solve(my_parsed.datasources.content, cache=cache),
        "This is some text.\n" +
        " A heading! \n" +
        " the bar!")

    eq_(solve(my_parsed.content_chars, cache=cache), 41)

    eq_(pickle.loads(pickle.dumps(my_parsed.content_chars)),
        my_parsed.content_chars)


def test_headings():

    cache = {my_text: "This is some text.\n" +
                      "== Heading! ==\n" +
                      "{{Foo}} the [[bar]]!\n" +
                      "=== Another heading! ==="}
    eq_(solve(my_parsed.datasources.heading_titles, cache=cache),
        ["Heading!", "Another heading!"])

    eq_(solve(my_parsed.headings, cache=cache), 2)

    eq_(solve(h_headings, cache=cache), 1)

    eq_(solve(lvl_2_headings, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(my_parsed.headings)), my_parsed.headings)
    eq_(pickle.loads(pickle.dumps(h_headings)), h_headings)
    eq_(pickle.loads(pickle.dumps(lvl_2_headings)), lvl_2_headings)


def test_wikilinks():

    cache = {my_text: "This is [[:en:some|text]].\n" +
                      "== Heading! ==\n" +
                      "{{Foo}} the [[bar]]!\n" +
                      "=== Another heading! ==="}
    eq_(solve(my_parsed.datasources.wikilink_titles, cache=cache),
        [":en:some", "bar"])

    eq_(solve(my_parsed.wikilinks, cache=cache), 2)

    eq_(solve(enwiki_wikilinks, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(my_parsed.wikilinks)), my_parsed.wikilinks)
    eq_(pickle.loads(pickle.dumps(enwiki_wikilinks)), enwiki_wikilinks)


def test_external_links():

    cache = {my_text: "This is [https://wikis.com].\n" +
                      "== Heading! ==\n" +
                      "{{Foo}} the [//meta.wikimedia.org foobar]!\n" +
                      "=== Another heading! ==="}
    eq_(solve(my_parsed.datasources.external_link_urls, cache=cache),
        ["https://wikis.com", "//meta.wikimedia.org"])

    eq_(solve(my_parsed.external_links, cache=cache), 2)

    eq_(solve(wikimedia_external_links, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(my_parsed.external_links)),
        my_parsed.external_links)
    eq_(pickle.loads(pickle.dumps(wikimedia_external_links)),
        wikimedia_external_links)


def test_tags():

    cache = {my_text: "This is [https://wikis.com].\n" +
                      "== Heading! ==\n" +
                      "<ref>Foo</ref> the <span>foobar</span>!\n" +
                      "=== Another heading! ==="}
    eq_(solve(my_parsed.datasources.tag_names, cache=cache),
        ["ref", "span"])

    eq_(solve(my_parsed.tags, cache=cache), 2)

    eq_(solve(ref_tags, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(my_parsed.tags)),
        my_parsed.tags)
    eq_(pickle.loads(pickle.dumps(ref_tags)),
        ref_tags)


def test_templates():

    cache = {my_text: "This is [https://wikis.com].\n" +
                      "== Heading! ==\n" +
                      "<ref>{{Cite thing}}</ref> the {{citation needed}}\n" +
                      "=== Another {{heading|foo}}! ==="}
    eq_(solve(my_parsed.datasources.template_names, cache=cache),
        ["Cite thing", "citation needed", "heading"])

    eq_(solve(my_parsed.templates, cache=cache), 3)

    eq_(solve(cite_templates, cache=cache), 1)

    eq_(pickle.loads(pickle.dumps(my_parsed.templates)),
        my_parsed.templates)
    eq_(pickle.loads(pickle.dumps(cite_templates)),
        cite_templates)
