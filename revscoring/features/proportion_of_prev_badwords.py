from .feature import Feature
from .modifiers import max
from .prev_badwords import prev_badwords
from .prev_words import prev_words

proportion_of_prev_badwords = prev_badwords/max(prev_words, 1)
