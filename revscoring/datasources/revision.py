import mwparserfromhell as mwp
from deltas.tokenizers import wikitext_split

from ..errors import RevisionNotFound
from .datasource import Datasource

id = Datasource("revision.id")
"""
Returns the `rev_id` of the current revision.
"""

metadata = Datasource("revision.metadata")
"""
Returns a :class:`~revscoring.datasources.types.RevisionMetadata` for the
current revision.
"""

text = Datasource("revision.text")
"""
Returns the text content of the current revision.
"""


# ############################### Tokenized ###################################
def process_tokens(revision_text):
    if revision_text is None:
        raise RevisionNotFound()
    return [t for t in wikitext_split.tokenize(revision_text)]

tokens = Datasource("revision.tokens",
                    process_tokens, depends_on=[text])
"""
Returns a list of tokens.
"""


# ################################ Parsed text ################################
def process_parse_tree(revision_text):
    if revision_text is None:
        raise RevisionNotFound()
    return mwp.parse(revision_text or "")

parse_tree = Datasource("revision.parse_tree",
                        process_parse_tree, depends_on=[text])
"""
Returns a :class:`mwparserfromhell.wikicode.Wikicode` abstract syntax tree
representing the content of the current revision.
"""


def process_content(revision_parse_tree):
    return revision_parse_tree.strip_code()

content = Datasource("revision.content", process_content,
                     depends_on=[parse_tree])
"""
Returns the raw content (no markup or templates) of the current revision.
"""


def process_content_tokens(revision_content):
    return wikitext_split.tokenize(revision_content)

content_tokens = Datasource("revision.content_tokens", process_content_tokens,
                            depends_on=[content])
"""
Returns tokens from the raw content (no markup or templates) of the current
revision
"""


def process_headings(revision_parse_tree):
    return revision_parse_tree.filter_headings()

headings = Datasource("revision.headings", process_headings,
                      depends_on=[parse_tree])
"""
Returns a list of :class:`mwparserfromhell.nodes.heading.Heading`'s present in
the content of the current revision.
"""


def process_internal_links(revision_parse_tree):
    return revision_parse_tree.filter_wikilinks()

internal_links = Datasource("revision.internal_links", process_internal_links,
                            depends_on=[parse_tree])
"""
Returns a list of :class:`mwparserfromhell.nodes.wikilink.Wikilink`'s present
in the content of the current revision.
"""


def process_tags(revision_parse_tree):
    return revision_parse_tree.filter_tags()

tags = Datasource("revision.tags", process_tags, depends_on=[parse_tree])
"""
Returns a list of html :class:`mwparserfromhell.nodes.tag.Tag`'s present in the
content of the current revision.
"""


def process_templates(revision_parse_tree):
    return revision_parse_tree.filter_templates()

templates = Datasource("revision.templates", process_templates,
                       depends_on=[parse_tree])
"""
Returns a list of html :class:`mwparserfromhell.nodes.template.Template`'s
present in the content of the current revision.
"""
