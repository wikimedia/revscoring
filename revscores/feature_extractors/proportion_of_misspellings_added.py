
from ..util.dependencies import depends
from ..util.returns import returns
from .misspellings_added import misspellings_added
from .words_added import words_added


@depends(on=[words_added, misspellings_added])
@returns(float)
def proportion_of_misspellings_added(words_added, misspellings_added):
    
    return misspellings_added/(words_added or 1)
