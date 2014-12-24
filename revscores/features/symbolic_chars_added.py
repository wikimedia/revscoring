import re

from ..datasources import contiguous_segments_added
from .feature import Feature

SYMBOLS = re.compile(r'[^\w\alpha\s]+', re.UNICODE)

def process(contiguous_segments_added):
    
    concat = "".join(contiguous_segments_added)
    
    sym_chars_added = 0
    
    for match in SYMBOLS.finditer(concat):
        sym_chars_added += len(match.group(0))
        
    
    return sym_chars_added

symbolic_chars_added = Feature("symbolic_chars_added", process,
                               returns=int,
                               depends_on=[contiguous_segments_added])
