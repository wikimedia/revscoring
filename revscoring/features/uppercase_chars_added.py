import re

from ..datasources import contiguous_segments_added
from .feature import Feature

UPPERCASE_RE = re.compile(r'[A-Z]+', re.UNICODE)
# TODO: Does not work for non-latin uppercase letters

def process(contiguous_segments_added):
    
    concat = "".join(contiguous_segments_added)
    
    chars_added = 0
    
    for match in UPPERCASE_RE.finditer(concat):
        chars_added += len(match.group(0))
        
    
    return chars_added

uppercase_chars_added = Feature("uppercase_chars_added", process,
                                returns=int,
                                depends_on=[contiguous_segments_added])
