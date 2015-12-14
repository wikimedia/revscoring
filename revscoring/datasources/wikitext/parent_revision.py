import re

import mwparserfromhell as mwp
from deltas.tokenizers import wikitext_split

from ..datasource import Datasource
from ..meta import filter, map, regex_matching
from ..parent_revision import text


def process_tokens(text):
    return [t for t in wikitext_split.tokenize(text or "")]

tokens = Datasource("wikitext.parent_revision.tokens",
                    process_tokens, depends_on=[text])
"""
Returns a list of tokens.
"""


def tokens_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.parent_revision.tokens_matching",
                       regex.pattern)

    return regex_matching(regex, tokens, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
that match a regular expression.
"""


def tokens_in_types(types, name=None):
    types = set(types)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.parent_revision.tokens_in_types",
                       types)

    return filter(lambda t: t.type in types, tokens, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
that are within a set of types.
"""


number_tokens = tokens_in_types(
    {'number'},
    name="wikitext.parent_revision.number_tokens"
)
"""
Returns a list of numeric tokens
"""

whitespace_tokens = tokens_in_types(
    {'whitespace'},
    name="wikitext.parent_revision.whitespace_tokens"
)
"""
Returns a list of whitespace tokens
"""

markup_tokens = tokens_in_types(
    {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close', 'tab_open',
     'tab_close', 'dcurly_open', 'dcurly_close', 'curly_open', 'curly_close',
     'bold', 'italics', 'equals'},
    name="wikitext.parent_revision.markup_tokens"
)
"""
Returns a list of markup tokens
"""

cjk_tokens = tokens_in_types(
    {'cjk'},
    name="wikitext.parent_revision.cjk_tokens"
)
"""
Returns a list of Chinese/Japanese/Korean tokens
"""

entity_tokens = tokens_in_types(
    {'entity'},
    name="wikitext.parent_revision.entity_tokens"
)
"""
Returns a list of HTML entity tokens
"""

url_tokens = tokens_in_types(
    {'url'},
    name="wikitext.parent_revision.url_tokens"
)
"""
Returns a list of URL tokens
"""

word_tokens = tokens_in_types(
    {'word'},
    name="wikitext.parent_revision.word_tokens"
)
"""
Returns a list of word tokens
"""

punctuation_tokens = tokens_in_types(
    {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon'},
    name="wikitext.parent_revision.punctuation_tokens"
)
"""
Returns a list of punctuation tokens
"""

break_tokens = tokens_in_types(
    {'break'},
    name="wikitext.parent_revision.break_tokens"
)
"""
Returns a list of break tokens
"""

def process_parse_tree(text):
    return mwp.parse(text or "")

parse_tree = Datasource("wikitext.parent_revision.parse_tree",
                        process_parse_tree, depends_on=[text])
"""
Returns a :class:`mwparserfromhell.wikicode.Wikicode` abstract syntax tree
representing the content of the revision.
"""


def process_content(revision_parse_tree):
    return revision_parse_tree.strip_code()

content = Datasource("wikitext.parent_revision.content", process_content,
                     depends_on=[parse_tree])
"""
Returns the raw content (no markup or templates) of the revision.
"""


def process_content_tokens(revision_content):
    return wikitext_split.tokenize(revision_content)

content_tokens = Datasource("wikitext.parent_revision.content_tokens",
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
               .format("wikitext.parent_revision.content_tokens_matching",
                       regex.pattern)

    return regex_matching(regex, content_tokens, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
that match a regular expression.
"""


def content_tokens_in_types(types, name=None, regex_flags=re.I):
    types = set(types)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.parent_revision.content_tokens_in_types",
                       types)

    return filter(lambda t: t.type in types, content_tokens, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
that are within a set of types.
"""


def process_headings(revision_parse_tree):
    return revision_parse_tree.filter_headings()

headings = Datasource("wikitext.parent_revision.headings", process_headings,
                      depends_on=[parse_tree])
"""
Returns a list of :class:`mwparserfromhell.nodes.heading.Heading`'s present in
the content of the revision.
"""


def extract_heading_title(heading):
    return str(heading.title).strip()

heading_titles = map(extract_heading_title, headings,
                     name="wikitext.parent_revision.heading_titles")
"""
Returns a list of heading titles
"""


def heading_titles_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.parent_revision.heading_titles_matching",
                       regex.pattern)

    return regex_matching(regex, heading_titles, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all header titles
that match a regular expression.
"""


def process_external_links(revision_parse_tree):
    return revision_parse_tree.filter_external_links()

external_links = Datasource("wikitext.parent_revision.external_links",
                            process_external_links,
                            depends_on=[parse_tree])
"""
Returns a list of :class:`mwparserfromhell.nodes.external_link.ExternalLink`'s
present in the content of the revision.
"""


def extract_external_link_url(elink):
    return str(elink.url)

external_link_urls = map(extract_external_link_url, external_links,
                         name="wikitext.parent_revision.external_link_url")
"""
Returns a list of string urls of external links (aka "targets")
"""


def external_link_urls_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.parent_revision.external_link_urls_matching",
                       regex.pattern)

    return regex_matching(regex, external_link_urls, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all external link URLs
that match a regular expression.
"""


def process_internal_links(revision_parse_tree):
    return revision_parse_tree.filter_wikilinks()

internal_links = Datasource("wikitext.parent_revision.internal_links",
                            process_internal_links,
                            depends_on=[parse_tree])
"""
Returns a list of :class:`mwparserfromhell.nodes.wikilink.Wikilink`'s present
in the content of the revision.
"""


def extract_internal_link_title(ilink):
    return str(ilink.title)

internal_link_titles = map(
    extract_internal_link_title,
    internal_links,
    name="wikitext.parent_revision.internal_link_titles"
)
"""
Returns a list of string titles of internal links (aka "targets")
"""


def internal_link_titles_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.parent_revision." +
                       "internal_link_titles_matching",
                       regex.pattern)

    return regex_matching(regex, internal_link_titles, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all internal link
titles names that match a regular expression.
"""


def process_tags(revision_parse_tree):
    return revision_parse_tree.filter_tags()

tags = Datasource("wikitext.parent_revision.tags", process_tags,
                  depends_on=[parse_tree])
"""
Returns a list of html :class:`mwparserfromhell.nodes.tag.Tag`'s present in
the content of the revision.
"""


def extract_tag_name(tag):
    return str(tag.tag)

tag_names = map(extract_tag_name, tags,
                name="wikitext.parent_revision.tag_names")
"""
Returns a list of html tag names present in the content of the revision
"""


def tag_names_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.parent_revision.tag_names_matching",
                       regex.pattern)

    return regex_matching(regex, tag_names, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all tag names that
match a regular expression.
"""


def process_templates(revision_parse_tree):
    return revision_parse_tree.filter_templates()

templates = Datasource("wikitext.parent_revision.templates", process_templates,
                       depends_on=[parse_tree])
"""
Returns a list of :class:`mwparserfromhell.nodes.template.Template`'s
present in the content of the revision.
"""


def extract_template_name(template):
    return str(template.name)

template_names = map(extract_template_name, templates,
                     name="wikitext.parent_revision.template_names")
"""
Returns a list of template names present in the content of the revision
"""


def template_names_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.parent_revision.template_names_matching",
                       regex.pattern)

    return regex_matching(regex, template_names, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all template names
that match a regular expression.
"""
