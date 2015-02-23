
from .modifiers import max
from .prev_misspellings import prev_misspellings
from .prev_words import prev_words

proportion_of_prev_misspellings = prev_misspellings/max(prev_words, 1)
