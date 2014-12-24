
from .feature import feature_processor
from .prev_badwords import prev_badwords
from .prev_words import prev_words


@feature_processor(returns=float,
                   depends_on=[prev_words, prev_badwords])
def proportion_of_prev_badwords(prev_words, prev_badwords):
    
    return prev_badwords/(prev_words or 1)
