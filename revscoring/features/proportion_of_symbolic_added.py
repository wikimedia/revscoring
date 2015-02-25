
from .chars_added import chars_added
from .modifiers import max
from .symbolic_chars_added import symbolic_chars_added

proportion_of_symbolic_added = symbolic_chars_added / max(chars_added, 1)
