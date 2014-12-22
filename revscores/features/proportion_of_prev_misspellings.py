
from .feature import feature_processor
from .prev_misspellings import prev_misspellings
from .prev_words import prev_words


@feature_processor(returns=float,
                   depends_on=[prev_words, prev_misspellings])
def proportion_of_prev_misspellings(prev_words, prev_misspellings):
    
    return prev_misspellings/(prev_words or 1)
