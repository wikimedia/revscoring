from .chars_added import chars_added
from .feature import Feature
from .modifiers import max
from .numeric_chars_added import numeric_chars_added

proportion_of_numeric_added = numeric_chars_added/max(chars_added, 1)
