from collections import namedtuple

from deltas import segment_matcher
from deltas.tokenizers import WikitextSplit

from .datasource import Datasource
from .previous_revision_text import previous_revision_text
from .revision_text import revision_text


def process(previous_revision_text, revision_text):
    previous_revision_text = previous_revision_text or ''
    revision_text = revision_text or ''
    
    tokenizer = WikitextSplit()
    
    a = tokenizer.tokenize(previous_revision_text)
    b = tokenizer.tokenize(revision_text)
    
    return [op for op in segment_matcher.diff(a, b)], a, b

revision_diff = Datasource("revision_diff", process,
                           depends_on=[previous_revision_text, revision_text])
