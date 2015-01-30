
from .chars_added import chars_added
from .feature import Feature
from .symbolic_chars_added import symbolic_chars_added


def process(chars_added, symbolic_chars_added):
    
    return symbolic_chars_added/(chars_added or 1)

proportion_of_symbolic_added = Feature("proportion_of_symbolic_added", process,
                                       returns=float,
                                       depends_on=[chars_added,
                                                   symbolic_chars_added])
