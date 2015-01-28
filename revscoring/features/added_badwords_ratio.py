from .feature import Feature
from .proportion_of_badwords_added import proportion_of_badwords_added
from .proportion_of_prev_badwords import proportion_of_prev_badwords


def process(proportion_of_badwords_added,
                         proportion_of_prev_badwords):
    
    return (proportion_of_badwords_added /
            (proportion_of_prev_badwords or 0.01))

added_badwords_ratio = Feature("added_badwords_ratio", process,
                               returns=float,
                               depends_on=[proportion_of_badwords_added,
                                           proportion_of_prev_badwords])
