import re

from ..datasources import contiguous_segments_added
from ..util.dependencies import depends
from ..util.returns import returns

NUMERIC_RE = re.compile(r'[0-9]+')

@depends(on=[contiguous_segments_added])
@returns(int)
def numeric_chars_added(contiguous_segments_added):
    
    concat = "".join(contiguous_segments_added)
    
    num_chars_added = 0
    
    for match in NUMERIC_RE.finditer(concat):
        num_chars_added += len(match.group(0))
        
    
    return num_chars_added
