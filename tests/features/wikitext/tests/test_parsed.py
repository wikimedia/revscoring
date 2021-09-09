import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.features.wikitext import revision

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
    assert (solve(revision.datasources.content, cache=cache) ==
            "This is some text.\n" +
            " A heading! \n" +
            " the bar!")

    assert solve(revision.content_chars, cache=cache) == 41

    assert (pickle.loads(pickle.dumps(revision.content_chars)) ==
            revision.content_chars)


def test_headings():

    cache = {r_text: "This is some text.\n" +
             "== Heading! ==\n" +
             "{{Foo}} the [[bar]]!\n" +
             "=== Another heading! ==="}
    assert (solve(revision.datasources.heading_titles, cache=cache) ==
            ["Heading!", "Another heading!"])

    assert solve(revision.headings, cache=cache) == 2

    assert solve(h_headings, cache=cache) == 1

    assert solve(lvl_2_headings, cache=cache) == 1

    assert pickle.loads(pickle.dumps(revision.headings)) == revision.headings
    assert pickle.loads(pickle.dumps(h_headings)) == h_headings
    assert pickle.loads(pickle.dumps(lvl_2_headings)) == lvl_2_headings


def test_wikilinks():

    cache = {r_text: "This is [[:en:some|text]].\n" +
             "== Heading! ==\n" +
             "{{Foo}} the [[bar]]!\n" +
             "=== Another heading! ==="}
    assert (solve(revision.datasources.wikilink_titles, cache=cache) ==
            [":en:some", "bar"])

    assert solve(revision.wikilinks, cache=cache) == 2

    assert solve(enwiki_wikilinks, cache=cache) == 1

    assert pickle.loads(pickle.dumps(revision.wikilinks)) == revision.wikilinks
    assert pickle.loads(pickle.dumps(enwiki_wikilinks)) == enwiki_wikilinks


def test_external_links():

    cache = {r_text: "This is [https://wikis.com].\n" +
             "== Heading! ==\n" +
             "{{Foo}} the [//meta.wikimedia.org foobar]!\n" +
             "=== Another heading! ==="}
    assert (solve(revision.datasources.external_link_urls, cache=cache) ==
            ["https://wikis.com", "//meta.wikimedia.org"])

    assert solve(revision.external_links, cache=cache) == 2

    assert solve(wikimedia_external_links, cache=cache) == 1

    assert (pickle.loads(pickle.dumps(revision.external_links)) ==
            revision.external_links)
    assert (pickle.loads(pickle.dumps(wikimedia_external_links)) ==
            wikimedia_external_links)


def test_tags():

    cache = {r_text: "This is [https://wikis.com].\n" +
             "== Heading! ==\n" +
             "<ref>Foo</ref> the <span>foobar</span>!\n" +
             "* item one\n" +
             "=== Another heading! ===\n" +
             "* item one\n" +
             "** item two\n"}
    print(solve(revision.datasources.tags_str, cache=cache))
    assert (solve(revision.datasources.tag_names, cache=cache) ==
            ["ref", "span", "li", "li", "li", "li"])
    # Note that the number of list items relates to the number of asterisks.

    assert solve(revision.tags, cache=cache) == 6

    assert solve(revision.ref_tags, cache=cache) == 1

    assert solve(revision.list_items, cache=cache) == 4

    assert (pickle.loads(pickle.dumps(revision.tags)) ==
            revision.tags)
    assert (pickle.loads(pickle.dumps(revision.ref_tags)) ==
            revision.ref_tags)
    assert (pickle.loads(pickle.dumps(revision.list_items)) ==
            revision.list_items)


def test_tags_str():

    cache = {r_text: "This is [https://wikis.com].\n" +
             "== Heading! ==\n" +
             "<ref>Foo</ref> the <span>foobar</span>!\n" +
             "=== Another heading! ==="}
    assert (solve(revision.datasources.tags_str, cache=cache) ==
            ["<ref>Foo</ref>", "<span>foobar</span>"])


def test_tags_str_matching():
    cache = {r_text: "This is [https://wikis.com].\n" +
                     "== Heading! ==\n" +
                     "<ref>{{Cite thing}}</ref> the {{citation needed}}\n" +
                     "=== Another {{heading|foo}}! ==="}

    ref = revision.datasources.tags_str_matching(
        r"<ref>.*</ref>", name="enwiki.revision.ref_tags")

    assert (solve(ref, cache=cache) ==
            ["<ref>{{Cite thing}}</ref>"])


def test_templates():

    cache = {r_text: "This is [https://wikis.com].\n" +
             "== Heading! ==\n" +
             "<ref>{{Cite thing}}</ref> the {{citation needed}}\n" +
             "=== Another {{heading|foo}}! ==="}
    assert (solve(revision.datasources.template_names, cache=cache) ==
            ["Cite thing", "citation needed", "heading"])

    assert solve(revision.templates, cache=cache) == 3

    assert solve(cite_templates, cache=cache) == 1

    assert (pickle.loads(pickle.dumps(revision.templates)) ==
            revision.templates)
    assert (pickle.loads(pickle.dumps(cite_templates)) ==
            cite_templates)


def test_templates_str():

    cache = {r_text: "This is [https://wikis.com].\n" +
             "== Heading! ==\n" +
             "<ref>{{Cite thing}}</ref> the {{citation needed}}\n" +
             "=== Another {{heading|foo}}! ==="}
    assert (solve(revision.datasources.templates_str, cache=cache) ==
            ["{{Cite thing}}", "{{citation needed}}", "{{heading|foo}}"])


def test_templates_str_matching():

    cache = {r_text: "This is [https://wikis.com].\n" +
             "== Heading! ==\n" +
             "<ref>{{Cite thing}}</ref> the {{citation needed}}\n" +
             "=== Another {{heading|foo}}! ==="}

    cite_template = revision.datasources.templates_str_matching(
        r"{{Cit.*}}", name="enwiki.revision.cite_template")

    assert (solve(cite_template, cache=cache) ==
            ["{{Cite thing}}", "{{citation needed}}"])
