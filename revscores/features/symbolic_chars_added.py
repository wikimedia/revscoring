import re

from ..datasources import contiguous_segments_added
from .feature import feature_processor

SYMBOLS = re.compile(r'[^\w\alpha\s]+')

@feature_processor(returns=int, depends_on=[contiguous_segments_added])
def symbolic_chars_added(contiguous_segments_added):
    
    concat = "".join(contiguous_segments_added)
    
    sym_chars_added = 0
    
    for match in SYMBOLS.finditer(concat):
        sym_chars_added += len(match.group(0))
        
    
    return sym_chars_added
