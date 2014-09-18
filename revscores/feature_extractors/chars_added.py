from ..datasources import contiguous_segments_added
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[contiguous_segments_added])
@returns(int)
def chars_added(contiguous_segments_added):
    
    return len("".join(contiguous_segments_added))
