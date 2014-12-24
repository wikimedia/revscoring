
from .chars_added import chars_added
from .feature import feature_processor
from .uppercase_chars_added import uppercase_chars_added


@feature_processor(returns=float,
                   depends_on=[chars_added, uppercase_chars_added])
def proportion_of_uppercase_added(chars_added, uppercase_chars_added):
    
    return uppercase_chars_added/(chars_added or 1)
