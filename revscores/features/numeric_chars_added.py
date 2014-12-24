import re

from ..datasources import contiguous_segments_added
from .feature import Feature

NUMERIC_RE = re.compile(r'[0-9]+')

def process(contiguous_segments_added):
    
    concat = "".join(contiguous_segments_added)
    
    chars_added = 0
    
    for match in NUMERIC_RE.finditer(concat):
        chars_added += len(match.group(0))
        
    
    return chars_added

numeric_chars_added = Feature("numeric_chars_added", process,
                              returns=int,
                              depends_on=[contiguous_segments_added])
