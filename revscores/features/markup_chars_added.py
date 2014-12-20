import re

from ..datasources import contiguous_segments_added
from .feature import feature_processor

MARKUP_RE = re.compile(r'(\[|\]|\{\||\|\}|\|-|\{\{|\}\})+')

@feature_processor(returns=int, depends_on=[contiguous_segments_added])
def markup_chars_added(contiguous_segments_added):
    
    concat = "".join(contiguous_segments_added)
    
    mk_chars_added = 0
    
    for match in MARKUP_RE.finditer(concat):
        mk_chars_added += len(match.group(0))
        
    
    return mk_chars_added
