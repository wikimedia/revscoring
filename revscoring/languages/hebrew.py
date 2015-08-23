import sys

from .space_delimited import SpaceDelimited

try:
    import enchant
    dictionary = enchant.Dict("he")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'he'.  " +
                      "Consider installing 'myspell-he'.")


badwords = [
    r"ה?קא?ק(י|ות|ה)",
    r"ה?חרא",
    r"חארות",
    r"[למ]חרבן",
    r"פיפי",
    r"(ב|ל|מ?ה)תחת",
    r"סקס",
    r"ה?זין",
    r"ציצים?",
    r"ה?בולבול(?:ים)?",
    r"זיו(ן|נים)",
    r"[מת]זד?יי(ן|נת|נים|נות|נו)",
    r"להזדיין",
    r"לזיין",
    r"למצוץ",
    r"מוצ(ץ|צת)",
    r"שפיך",
    r"ה?דפוק(ה|ים)?",
    r"ה?הומו",
    r"ה?גיי",
    r"קוקסינל",
    r"סקסי",
    r"יבני",
    r"ה?זונ(ה|ות)",
    r"בנזונה",
    r"שרמוט(ה|ות)",
    r"ה?מניאק",
    r"ה?מטומט(ם|מת|מי)",
    r"דביל(?:ים)?",
    r"טמבל",
    r"מפגר(?:ים)?",
    r"ה?מהממת",
    r"ה?כוס(ון|ית|יות)",
    r"אחושרמוטה",
    r"ה?פלו(ץ|צים)",
    r"[המ]פלי(ץ|צה)",
    r"להפליץ",
    r"מסריח(ים|ה)?",
    r"מגעיל",
    r"נוד",
    r"שטויות",
    r"היוש",
    r"חיימשלי",
    r"כאפות",
    r"כפרע",
    r"דגכ",
    r"זובי"
]
informals = [
    r"חחח+",
    r"[בה]ייי",
    r"פהה+",
    r"מכוערת?",
    r"מעפ(ן|נה)",
    r"ו?חתיך",
    r"אחלה",
    r"ה?חמוד(ה|ים)?",
    r"יאלל?ה",
    r"טעים",
    r"(בלה)+",
    r"סתם",
    r"כנסו",
    r"אות(כם|ך+)",
    r"שתדע",
    r"תהנו",
    r"לכו",
    r"לכם",
    r"בגללך",
    r"עליי",
    r"של(יי|כם|ך)",
    r"תיכנסו",
    r"אתם",
    r"אוהבת",
    r"מגניב",
    r"כיף",
    r"הדגדגנים",
    r"חזיות",
    r"[בל]פורנוגרפיה",
    r"משו?עמ(מים|ם)",
    r"אהה",
    r"יימח"
]

sys.modules[__name__] = SpaceDelimited(
    __name__,
    doc="""
hebrew
======

revision
--------
.. autoattribute:: revision.words
.. autoattribute:: revision.content_words
.. autoattribute:: revision.badwords
.. autoattribute:: revision.misspellings
.. autoattribute:: revision.informals

parent_revision
---------------
.. autoattribute:: parent_revision.words
.. autoattribute:: parent_revision.content_words
.. autoattribute:: parent_revision.badwords
.. autoattribute:: parent_revision.misspellings
.. autoattribute:: parent_revision.informals

diff
----
.. autoattribute:: diff.words_added
.. autoattribute:: diff.words_removed
.. autoattribute:: diff.badwords_added
.. autoattribute:: diff.badwords_removed
.. autoattribute:: diff.misspellings_added
.. autoattribute:: diff.misspellings_removed
.. autoattribute:: diff.informals_added
.. autoattribute:: diff.informals_removed
    """,
    badwords=badwords,
    dictionary=dictionary,
    informals=informals
)
