import warnings

import enchant

from .language import Language, LanguageUtility

DICTIONARY = enchant.Dict("fa")
BADWORDS = set([
    "کیرم", "ایتالیک", "کونی", "کیر", "فرمود", "آله", "فرموده", "فرمودند",
    "جنده", "برووتو", "لعنت", "کون", "السلام", "جمهورمحترم", "کونی",
    "کاکاسیاه", "آشغال", "گائیدم", "گوزیده", "مشنگ", "ننتو", "بخواب"
])


def is_misspelled_process():
    def is_misspelled(word):
        return not DICTIONARY.check(word)
    return is_misspelled


def is_badword_process():
    def is_badword(word):
        return word.lower() in BADWORDS
    return is_badword


is_badword = LanguageUtility("is_badword", is_badword_process, depends_on=[])
is_misspelled = LanguageUtility("is_misspelled", is_misspelled_process,
                                depends_on=[])

persian = Language("revscoring.languages.persian", [is_badword, is_misspelled])
"""
Implements :class:`~revscoring.languages.language.Language` for Persian/Farsi.
:data:`~revscoring.languages.language.is_badword` and
:data:`~revscoring.languages.language.is_misspelled` are provided.
"""
