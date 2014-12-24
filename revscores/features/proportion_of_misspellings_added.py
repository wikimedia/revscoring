
from .feature import feature_processor
from .misspellings_added import misspellings_added
from .words_added import words_added


@feature_processor(returns=float,
                   depends_on=[words_added, misspellings_added])
def proportion_of_misspellings_added(words_added, misspellings_added):
    
    return misspellings_added/(words_added or 1)
