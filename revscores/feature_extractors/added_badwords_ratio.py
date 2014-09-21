
from ..util.dependencies import depends
from ..util.returns import returns
from .proportion_of_badwords_added import proportion_of_badwords_added
from .proportion_of_prev_badwords import proportion_of_prev_badwords


@depends(on=[proportion_of_badwords_added, proportion_of_prev_badwords])
@returns(float)
def added_badwords_ratio(proportion_of_badwords_added,
                         proportion_of_prev_badwords):
    
    return proportion_of_badwords_added /\
           (proportion_of_prev_badwords or 0.01)
