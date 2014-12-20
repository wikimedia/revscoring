
from .feature import feature_processor
from .proportion_of_misspellings_added import proportion_of_misspellings_added
from .proportion_of_prev_misspellings import proportion_of_prev_misspellings


@feature_processor(returns=float,
                   depends_on=[proportion_of_misspellings_added,
                               proportion_of_prev_misspellings])
def added_misspellings_ratio(proportion_of_misspellings_added,
                             proportion_of_prev_misspellings):
    
    return (proportion_of_misspellings_added /
            (proportion_of_prev_misspellings or 0.01))
