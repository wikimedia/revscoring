
from .badwords_added import badwords_added
from .feature import feature_processor
from .words_added import words_added


@feature_processor(returns=float,
                   depends_on=[words_added, badwords_added])
def proportion_of_badwords_added(words_added, badwords_added):
    
    return badwords_added/(words_added or 1)
