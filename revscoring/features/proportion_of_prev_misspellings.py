
from .feature import Feature
from .prev_misspellings import prev_misspellings
from .prev_words import prev_words


def process(prev_words, prev_misspellings):
    
    return prev_misspellings/(prev_words or 1)

proportion_of_prev_misspellings = Feature("proportion_of_prev_misspellings",
                                          process,
                                          returns=float,
                                          depends_on=[prev_words,
                                                      prev_misspellings])
