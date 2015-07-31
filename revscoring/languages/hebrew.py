import re
import sys

import enchant

from .language import Language, LanguageUtility

BAD_REGEXES = [
    'ה?קא?ק(י|ות|ה)',
    'ה?חרא',
    'חארות',
    '[למ]חרבן',
    'פיפי',
    '(ב|ל|מ?ה)תחת',
    'סקס',
    'ה?זין',
    'ציצים?',
    'ה?בולבול(?:ים)?',
    'זיו(ן|נים)',
    '[מת]זד?יי(ן|נת|נים|נות|נו)',
    'להזדיין',
    'לזיין',
    'למצוץ',
    'מוצ(ץ|צת)',
    'שפיך',
    'ה?דפוק(ה|ים)?',
    'ה?הומו',
    'ה?גיי',
    'קוקסינל',
    'סקסי',
    'יבני',
    'ה?זונ(ה|ות)',
    'בנזונה',
    'שרמוט(ה|ות)',
    'ה?מניאק',
    'ה?מטומט(ם|מת|מי)',
    'דביל(?:ים)?',
    'טמבל',
    'מפגר(?:ים)?',
    'ה?מהממת',
    'ה?כוס(ון|ית|יות)',
    'אחושרמוטה',
    'ה?פלו(ץ|צים)',
    '[המ]פלי(ץ|צה)',
    'להפליץ',
    'מסריח(ים|ה)?',
    'מגעיל',
    'נוד',
    'שטויות'
    'היוש',
    'חיימשלי',
    'כאפות',
    'כפרע',
    'דגכ',
    'זובי'
]
INFORMAL_REGEXES = [
    'חחח+',
    '[בה]ייי',
    'פהה+',
    'מכוערת?',
    'מעפ(ן|נה)',
    'ו?חתיך',
    'אחלה',
    'ה?חמוד(ה|ים)?',
    'יאלל?ה',
    'טעים',
    '(בלה)+',
    'סתם',
    'כנסו',
    'אות(כם|ך+)',
    'שתדע',
    'תהנו',
    'לכו',
    'לכם',
    'בגללך',
    'עליי',
    'של(יי|כם|ך)',
    'תיכנסו',
    'אתם',
    'אוהבת',
    'מגניב',
    'כיף',
    'הדגדגנים',
    'חזיות',
    '[בל]פורנוגרפיה',
    'משו?עמ(מים|ם)',
    'אהה',
    'יימח'
]
BAD_REGEX = re.compile("|".join(BAD_REGEXES))
INFORMAL_REGEX = re.compile("|".join(INFORMAL_REGEXES))
DICTIONARY = enchant.Dict("he")

def is_badword_process():
    def is_badword(word):
        return bool(BAD_REGEX.match(word.lower()))

    return is_badword


is_badword = LanguageUtility("is_badword", is_badword_process)


def is_informal_word_process():
    def is_informal_word(word):
        return bool(INFORMAL_REGEX.match(word.lower()))

    return is_informal_word


is_informal_word = LanguageUtility("is_informal_word",
                                   is_informal_word_process)


def is_misspelled_process():
    def is_misspelled(word):
        return not DICTIONARY.check(word)

    return is_misspelled


is_misspelled = LanguageUtility("is_misspelled", is_misspelled_process)



sys.modules[__name__] = Language(
    __name__,
    [is_badword, is_misspelled, is_informal_word]
)
"""
Implements :class:`~revscoring.languages.language.Language` for Hebrew.
"""
