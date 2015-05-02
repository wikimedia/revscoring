import warnings

import enchant

from .language import Language, LanguageUtility

DICTIONARY = enchant.Dict("fa")

def is_misspelled_process():
    def is_misspelled(word):
        return not DICTIONARY.check(word)
    return is_misspelled

is_misspelled = LanguageUtility("is_misspelled", is_misspelled_process,
                                depends_on=[])

english = Language("revscoring.languages.english", [is_misspelled])
