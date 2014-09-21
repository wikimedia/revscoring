
from ..util.dependencies import depends
from ..util.returns import returns
from .chars_added import chars_added
from .symbolic_chars_added import symbolic_chars_added


@depends(on=[chars_added, symbolic_chars_added])
@returns(float)
def proportion_of_symbolic_added(chars_added, symbolic_chars_added):
    
    return symbolic_chars_added/(chars_added or 1)
