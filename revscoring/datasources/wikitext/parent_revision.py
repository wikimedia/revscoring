import re

import mwparserfromhell as mwp
from deltas.tokenizers import wikitext_split

from ..datasource import Datasource
from ..meta import ItemFilter, ItemMapper, TokensMatching
from ..parent_revision import text


def process_tokens(text):
    return [t for t in wikitext_split.tokenize(text or "")]

tokens = Datasource("revision.tokens",
                    process_tokens, depends_on=[text])
"""
Returns a list of tokens.
"""


def tokens_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.tokens_matching",
                       regex.pattern)

    return TokensMatching(name, tokens, regex)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
that match a regular expression.
"""


def tokens_in_types(types, name=None):
    types = set(types)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.tokens_in_types",
                       types)

    return ItemFilter(name, tokens, lambda t: t.type in types)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
that are within a set of types.
"""


words = tokens_in_types({'words'}, name="wikitext.revision.words")
"""
Generates a list of word-tokens.
"""


def process_parse_tree(text):
    return mwp.parse(text or "")

parse_tree = Datasource("wikitext.revision.parse_tree",
                        process_parse_tree, depends_on=[text])
"""
Returns a :class:`mwparserfromhell.wikicode.Wikicode` abstract syntax tree
representing the content of the revision.
"""


def process_content(revision_parse_tree):
    return revision_parse_tree.strip_code()

content = Datasource("wikitext.revision.content", process_content,
                     depends_on=[parse_tree])
"""
Returns the raw content (no markup or templates) of the revision.
"""


def process_content_tokens(revision_content):
    return wikitext_split.tokenize(revision_content)

content_tokens = Datasource("wikitext.revision.content_tokens",
                            process_content_tokens,
                            depends_on=[content])
"""
Returns tokens from the raw content (no markup or templates) of the current
revision
"""


def content_tokens_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.content_tokens_matching",
                       regex.pattern)

    return TokensMatching(name, content_tokens, regex)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
that match a regular expression.
"""


def content_tokens_in_types(types, name=None, regex_flags=re.I):
    types = set(types)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.content_tokens_in_types",
                       types)

    return ItemFilter(name, content_tokens, lambda t: t.type in types)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
that are within a set of types.
"""


content_words = content_tokens_in_types({'words'},
                                        name="wikitext.revision.content_words")
"""
Generates a list of word-tokens within content.
"""


def process_headings(revision_parse_tree):
    return revision_parse_tree.filter_headings()

headings = Datasource("wikitext.revision.headings", process_headings,
                      depends_on=[parse_tree])
"""
Returns a list of :class:`mwparserfromhell.nodes.heading.Heading`'s present in
the content of the revision.
"""


def extract_heading_title(heading):
    return str(heading.title)

heading_titles = ItemMapper("wikitext.revision.heading_titles",
                            headings,
                            extract_heading_title)
"""
Returns a list of heading titles
"""


def heading_titles_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.heading_titles_matching",
                       regex.pattern)

    return TokensMatching(name, heading_titles, regex)
"""
Constructs a :class:`revscoring.Datasource` that returns all header titles
that match a regular expression.
"""


def process_external_links(revision_parse_tree):
    return revision_parse_tree.filter_external_links()

external_links = Datasource("wikitext.revision.external_links",
                            process_external_links,
                            depends_on=[parse_tree])
"""
Returns a list of :class:`mwparserfromhell.nodes.external_link.ExternalLink`'s
present in the content of the revision.
"""


def extract_external_link_url(elink):
    return str(elink.url)

external_link_urls = ItemMapper("wikitext.revision.external_link_url",
                                external_links,
                                extract_external_link_url)
"""
Returns a list of string urls of external links (aka "targets")
"""


def external_link_urls_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.external_link_urls_matching",
                       regex.pattern)

    return TokensMatching(name, external_link_urls, regex)
"""
Constructs a :class:`revscoring.Datasource` that returns all external link URLs
that match a regular expression.
"""


def process_internal_links(revision_parse_tree):
    return revision_parse_tree.filter_wikilinks()

internal_links = Datasource("wikitext.revision.internal_links",
                            process_internal_links,
                            depends_on=[parse_tree])
"""
Returns a list of :class:`mwparserfromhell.nodes.wikilink.Wikilink`'s present
in the content of the revision.
"""


def extract_internal_link_title(ilink):
    return str(ilink.title)

internal_link_titles = ItemMapper("wikitext.revision.internal_link_titles",
                                  internal_links,
                                  extract_internal_link_title)
"""
Returns a list of string titles of internal links (aka "targets")
"""


def internal_link_titles_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.internal_link_titles_matching",
                       regex.pattern)

    return TokensMatching(name, internal_link_titles, regex)
"""
Constructs a :class:`revscoring.Datasource` that returns all internal link
titles names that match a regular expression.
"""


def process_tags(revision_parse_tree):
    return revision_parse_tree.filter_tags()

tags = Datasource("wikitext.revision.tags", process_tags,
                  depends_on=[parse_tree])
"""
Returns a list of html :class:`mwparserfromhell.nodes.tag.Tag`'s present in the
content of the revision.
"""


def extract_tag_name(tag):
    return str(tag.name)

tag_names = ItemMapper("wikitext.revision.tag_names", tags,
                       extract_tag_name)
"""
Returns a list of html tag names present in the content of the revision
"""


def tag_names_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.tag_names_matching", regex.pattern)

    return TokensMatching(name, tag_names, regex)
"""
Constructs a :class:`revscoring.Datasource` that returns all tag names that
match a regular expression.
"""


def process_templates(revision_parse_tree):
    return revision_parse_tree.filter_templates()

templates = Datasource("wikitext.revision.templates", process_templates,
                       depends_on=[parse_tree])
"""
Returns a list of :class:`mwparserfromhell.nodes.template.Template`'s
present in the content of the revision.
"""


def extract_template_name(template):
    return str(template.name)
template_names = ItemMapper("wikitext.revision.template_names", templates,
                            extract_template_name)
"""
Returns a list of template names present in the content of the revision
"""


def template_names_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.template_names_matching",
                       regex.pattern)

    return TokensMatching(name, template_names, regex)
"""
Constructs a :class:`revscoring.Datasource` that returns all template names
that match a regular expression.
"""
