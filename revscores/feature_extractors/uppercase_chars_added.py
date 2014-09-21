import re

from ..datasources import contiguous_segments_added
from ..util.dependencies import depends
from ..util.returns import returns

UPPERCASE_RE = re.compile(r'[A-Z]+')
# TODO: Does not work for non-latin uppercase letters

@depends(on=[contiguous_segments_added])
@returns(int)
def uppercase_chars_added(contiguous_segments_added):
    
    concat = "".join(contiguous_segments_added)
    
    chars_added = 0
    
    for match in UPPERCASE_RE.finditer(concat):
        chars_added += len(match.group(0))
        
    
    return chars_added
