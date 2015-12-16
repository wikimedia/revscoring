from deltas import wikitext_split

from ....datasources import Datasource


def process_tokens(text):
    return [t for t in wikitext_split.tokenize(text)]


def tokenized(text_datasource, name=None):
    """
    Constructs a :class:`revision.Datasource` that generates a list of tokens
    """
    if name is None:
        name = "{0}({1})".format("tokenized", text_datasource)

    return Datasource(
        name, process_tokens, depends_on=[text_datasource]
    )
