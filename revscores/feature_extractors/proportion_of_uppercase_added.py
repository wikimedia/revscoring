
from ..util.dependencies import depends
from ..util.returns import returns
from .chars_added import chars_added
from .uppercase_chars_added import uppercase_chars_added


@depends(on=[chars_added, uppercase_chars_added])
@returns(float)
def proportion_of_uppercase_added(chars_added, uppercase_chars_added):
    
    return uppercase_chars_added/(chars_added or 1)
