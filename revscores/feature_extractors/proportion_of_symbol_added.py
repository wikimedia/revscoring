
from ..util.dependencies import depends
from ..util.returns import returns
from .chars_added import chars_added
from .symbol_chars_added import symbol_chars_added


@depends(on=[chars_added, symbol_chars_added])
@returns(float)
def proportion_of_symbol_added(chars_added, symbol_chars_added):
    
    return symbol_chars_added/(chars_added or 1)
