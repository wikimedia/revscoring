import re

from ..datasources import contiguous_segments_added
from .feature import Feature

MARKUP_RE = re.compile(r'(\[|\]|\{\||\|\}|\|-|\{\{|\}\})+')

def process(contiguous_segments_added):
    
    concat = "".join(contiguous_segments_added)
    
    mk_chars_added = 0
    
    for match in MARKUP_RE.finditer(concat):
        mk_chars_added += len(match.group(0))
        
    
    return mk_chars_added

markup_chars_added = Feature("markup_chars_added", process,
                             returns=int,
                             depends_on=[contiguous_segments_added])
