import re
import sys

import enchant

from .language import RegexLanguage

badwords = [
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
informals = [
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
try:
    dictionary = enchant.Dict("he")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'he'.  " +
                      "Consider installing 'myspell-he'.")



sys.modules[__name__] = RegexLanguage(
    __name__,
    badwords=badwords,
    informals=informals,
    dictionary=dictionary
)
"""
Implements :class:`~revscoring.languages.language.RegexLanguage` for Hebrew.
:data:`~revscoring.languages.language.is_badword`,
:data:`~revscoring.languages.language.is_misspelled`, and
:data:`~revscoring.languages.language.is_informal_word` are provided.
"""
