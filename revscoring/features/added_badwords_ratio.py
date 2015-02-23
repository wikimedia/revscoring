from .modifiers import max
from .proportion_of_badwords_added import proportion_of_badwords_added
from .proportion_of_prev_badwords import proportion_of_prev_badwords

added_badwords_ratio = proportion_of_badwords_added / \
                       max(proportion_of_prev_badwords, 0.01)
