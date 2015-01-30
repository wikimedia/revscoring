
from .chars_added import chars_added
from .feature import Feature
from .markup_chars_added import markup_chars_added


def process(chars_added, markup_chars_added):
    
    return markup_chars_added/(chars_added or 1)

proportion_of_markup_added = Feature("proportion_of_markup_added", process,
                                     returns=float,
                                     depends_on=[chars_added,
                                                 markup_chars_added])
