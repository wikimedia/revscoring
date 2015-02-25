
from .chars_added import chars_added
from .markup_chars_added import markup_chars_added
from .modifiers import max

proportion_of_markup_added = markup_chars_added/max(chars_added, 1)
