
from ..util.dependencies import depends
from ..util.returns import returns
from .chars_added import chars_added
from .numeric_chars_added import numeric_chars_added


@depends(on=[chars_added, numeric_chars_added])
@returns(float)
def proportion_of_numeric_added(chars_added, numeric_chars_added):
    
    return numeric_chars_added/(chars_added or 1)
