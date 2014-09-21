
from ..util.dependencies import depends
from ..util.returns import returns
from .prev_misspellings import prev_misspellings
from .prev_words import prev_words


@depends(on=[prev_words, prev_misspellings])
@returns(float)
def proportion_of_prev_misspellings(prev_words, prev_misspellings):
    
    return prev_misspellings/(prev_words or 1)
