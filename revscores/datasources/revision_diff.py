from collections import namedtuple

from deltas import segment_matcher
from deltas.tokenizers import WikitextSplit

from ..util.dependencies import depends_on
from .previous_revision_text import previous_revision_text
from .revision_text import revision_text


@depends_on(previous_revision_text, revision_text)
def revision_diff(previous_revision_text, revision_text):
    tokenizer = WikitextSplit()
    
    a = tokenizer.tokenize(previous_revision_text)
    b = tokenizer.tokenize(revision_text)
    
    return (segment_matcher.diff(a, b), a, b)
