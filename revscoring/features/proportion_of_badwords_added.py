
from .badwords_added import badwords_added
from .modifiers import max
from .words_added import words_added

proportion_of_badwords_added = badwords_added/max(words_added, 1)
