import re

from ..datasources import contiguous_segments_added
from .feature import feature_processor

NUMERIC_RE = re.compile(r'[0-9]+')

@feature_processor(returns=int,
                   depends_on=[contiguous_segments_added])
def numeric_chars_added(contiguous_segments_added):
    
    concat = "".join(contiguous_segments_added)
    
    chars_added = 0
    
    for match in NUMERIC_RE.finditer(concat):
        chars_added += len(match.group(0))
        
    
    return chars_added
