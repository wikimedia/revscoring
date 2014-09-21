
from ..util.dependencies import depends
from ..util.returns import returns
from .badwords_added import badwords_added
from .words_added import words_added


@depends(on=[words_added, badwords_added])
@returns(float)
def proportion_of_badwords_added(words_added, badwords_added):
    
    return badwords_added/(words_added or 1)
