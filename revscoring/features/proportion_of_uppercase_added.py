
from .chars_added import chars_added
from .modifiers import max
from .uppercase_chars_added import uppercase_chars_added

proportion_of_uppercase_added = uppercase_chars_added/max(chars_added, 1)
