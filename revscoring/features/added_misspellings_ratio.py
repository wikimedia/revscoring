
from .feature import Feature
from .proportion_of_misspellings_added import proportion_of_misspellings_added
from .proportion_of_prev_misspellings import proportion_of_prev_misspellings


def process(proportion_of_misspellings_added,
                             proportion_of_prev_misspellings):
    
    return (proportion_of_misspellings_added /
            (proportion_of_prev_misspellings or 0.01))

added_misspellings_ratio = Feature("added_misspellings_ratio", process,
                                   returns=float,
                                   depends_on=[proportion_of_misspellings_added,
                                               proportion_of_prev_misspellings])
