from ..datasources import contiguous_segments_removed
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[contiguous_segments_removed])
@returns(int)
def segments_removed(contiguous_segments_removed):
    return len(contiguous_segments_removed)
