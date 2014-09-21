
from ..util.dependencies import depends
from ..util.returns import returns
from .prev_badwords import prev_badwords
from .prev_words import prev_words


@depends(on=[prev_words, prev_badwords])
@returns(float)
def proportion_of_prev_badwords(prev_words, prev_badwords):
    
    return prev_badwords/(prev_words or 1)
