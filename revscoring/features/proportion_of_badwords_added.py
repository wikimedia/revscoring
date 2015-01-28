
from .badwords_added import badwords_added
from .feature import Feature
from .words_added import words_added


def process(words_added, badwords_added):
    
    return badwords_added/(words_added or 1)

proportion_of_badwords_added = Feature("proportion_of_badwords_added", process,
                                       returns=float,
                                       depends_on=[words_added, badwords_added])
