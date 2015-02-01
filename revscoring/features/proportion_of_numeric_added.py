
from .chars_added import chars_added
from .feature import Feature
from .numeric_chars_added import numeric_chars_added


def process(chars_added, numeric_chars_added):
    
    return numeric_chars_added/(chars_added or 1)

proportion_of_numeric_added = Feature("proportion_of_numeric_added", process,
                                      returns=float,
                                      depends_on=[chars_added,
                                                  numeric_chars_added])
