from collections import namedtuple

from mw import Timestamp

import mwparserfromhell as mwp

from ..errors import RevisionDocumentNotFound
from .datasource import Datasource
from .types import RevisionMetadata
from .util import WORD_RE


def process_doc(rev_id, session):
    try:
        doc = session.revisions.get(rev_id=rev_id,
                                    properties={'ids', 'user', 'timestamp',
                                                'userid', 'comment', 'content',
                                                'flags', 'size'})
        return doc
    except KeyError:
        raise RevisionDocumentNotFound({'rev_id': rev_id})

doc = Datasource("revision.doc", process_doc, depends_on=['rev_id', 'session'])


def process_metadata(revision_doc):
    return RevisionMetadata.from_doc(revision_doc)

metadata = Datasource("revision.metadata", process_metadata, depends_on=[doc])


def process_text(revision_doc):
    return revision_doc.get("*", "")

text = Datasource("revision.text", process_text, depends_on=[doc])


def process_words(revision_text):
    return [m.group(0) for m in WORD_RE.finditer(revision_text)]

words = Datasource("revision.words", process_words, depends_on=[text])


################################# Parsed text ################################


def process_parse_tree(revision_text):
    return mwp.parse(revision_text or "")

parse_tree = Datasource("revision.parse_tree",
                        process_parse_tree, depends_on=[text])


def process_content(revision_parse_tree):
    return revision_parse_tree.strip_code()

content = Datasource("revision.content", process_content,
                     depends_on=[parse_tree])


def process_content_words(content):
    return [m.group(0) for m in WORD_RE.finditer(content)]

content_words = Datasource("revision.content_words", process_content_words,
                           depends_on=[content])


def process_headings(revision_parse_tree):
    return revision_parse_tree.filter_headings()

headings = Datasource("revision.headings", process_headings,
                      depends_on=[parse_tree])


def process_internal_links(revision_parse_tree):
    return revision_parse_tree.filter_wikilinks()

internal_links = Datasource("revision.internal_links", process_internal_links,
                            depends_on=[parse_tree])


def process_tags(revision_parse_tree):
    return revision_parse_tree.filter_tags()

tags = Datasource("revision.tags", process_tags, depends_on=[parse_tree])


def process_templates(revision_parse_tree):
    return revision_parse_tree.filter_templates()

templates = Datasource("revision.templates", process_templates,
                       depends_on=[parse_tree])
