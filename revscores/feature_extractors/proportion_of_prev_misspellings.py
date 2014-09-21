
from ..util.dependencies import depends
from ..util.returns import returns
from .misspellings_added import misspellings_added
from .words_added import words_added


@depends(on=[prev_words, prev_misspellings])
@returns(float)
def proportion_of_misspellings_added(prev_words, prev_misspellings):
    
    return prev_misspellings/(prev_words or 1)
