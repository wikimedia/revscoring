import re

from ..datasources import contiguous_segments_added
from ..util.dependencies import depends
from ..util.returns import returns

SYMBOLS = re.compile(r'[^\w\alpha\s]+')

@depends(on=[contiguous_segments_added])
@returns(int)
def symbol_chars_added(contiguous_segments_added):
    
    concat = "".join(contiguous_segments_added)
    
    sym_chars_added = 0
    
    for match in SYMBOLS.finditer(concat):
        sym_chars_added += len(match.group(0))
        
    
    return sym_chars_added
