

from .feature import feature_processor
from .proportion_of_badwords_added import proportion_of_badwords_added
from .proportion_of_prev_badwords import proportion_of_prev_badwords


@feature_processor(returns=float,
                   depends_on=[proportion_of_badwords_added,
                               proportion_of_prev_badwords])
def added_badwords_ratio(proportion_of_badwords_added,
                         proportion_of_prev_badwords):
    
    return (proportion_of_badwords_added /
            (proportion_of_prev_badwords or 0.01))
