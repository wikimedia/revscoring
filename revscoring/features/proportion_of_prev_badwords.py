
from .feature import Feature
from .prev_badwords import prev_badwords
from .prev_words import prev_words


def process(prev_words, prev_badwords):
    
    return prev_badwords/(prev_words or 1)

proportion_of_prev_badwords = Feature("proportion_of_prev_badwords", process,
                                      returns=float,
                                      depends_on=[prev_words, prev_badwords])
