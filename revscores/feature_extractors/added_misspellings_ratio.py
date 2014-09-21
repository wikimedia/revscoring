
from ..util.dependencies import depends
from ..util.returns import returns
from .proportion_of_misspellings_added import proportion_of_misspellings_added
from .proportion_of_prev_misspellings import proportion_of_prev_misspellings


@depends(on=[proportion_of_misspellings_added, proportion_of_prev_misspellings])
@returns(float)
def added_misspellings_ratio(proportion_of_misspellings_added,
                             proportion_of_prev_misspellings):
    
    return proportion_of_misspellings_added /\
           (proportion_of_prev_misspellings or 0.01)
