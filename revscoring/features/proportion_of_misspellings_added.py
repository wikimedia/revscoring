from .feature import Feature
from .misspellings_added import misspellings_added
from .words_added import words_added


def process(words_added, misspellings_added):
    
    return misspellings_added/(words_added or 1)

proportion_of_misspellings_added = Feature("proportion_of_misspellings_added",
                                           process,
                                           returns=float,
                                           depends_on=[words_added,
                                                       misspellings_added])
