
from .chars_added import chars_added
from .feature import Feature
from .uppercase_chars_added import uppercase_chars_added


def process(chars_added, uppercase_chars_added):
    
    return uppercase_chars_added/(chars_added or 1)

proportion_of_uppercase_added = Feature("proportion_of_uppercase_added",
                                        process,
                                        returns=float,
                                        depends_on=[chars_added,
                                                    uppercase_chars_added])
