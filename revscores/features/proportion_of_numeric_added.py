
from .chars_added import chars_added
from .feature import feature_processor
from .numeric_chars_added import numeric_chars_added


@feature_processor(returns=float,
                   depends_on=[chars_added, numeric_chars_added])
def proportion_of_numeric_added(chars_added, numeric_chars_added):
    
    return numeric_chars_added/(chars_added or 1)
