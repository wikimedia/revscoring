from .feature import Feature
from .misspellings_added import misspellings_added
from .modifiers import max
from .words_added import words_added

proportion_of_misspellings_added = misspellings_added/max(words_added, 1)
