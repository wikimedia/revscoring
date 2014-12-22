
from .chars_added import chars_added
from .feature import feature_processor
from .markup_chars_added import markup_chars_added


@feature_processor(returns=float,
                   depends_on=[chars_added, markup_chars_added])
def proportion_of_markup_added(chars_added, markup_chars_added):
    
    return markup_chars_added/(chars_added or 1)
