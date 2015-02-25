from .modifiers import max
from .proportion_of_misspellings_added import proportion_of_misspellings_added
from .proportion_of_prev_misspellings import proportion_of_prev_misspellings

added_misspellings_ratio = proportion_of_misspellings_added / \
                           max(proportion_of_prev_misspellings, 0.01)
