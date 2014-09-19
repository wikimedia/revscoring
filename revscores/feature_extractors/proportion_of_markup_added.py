
from ..util.dependencies import depends
from ..util.returns import returns
from .chars_added import chars_added
from .markup_chars_added import markup_chars_added


@depends(on=[chars_added, markup_chars_added])
@returns(float)
def proportion_of_markup_added(chars_added, markup_chars_added):
    
    return markup_chars_added/(chars_added or 1)
