from hanziconv import HanziConv

from .features import RegexMatches

name = "chinese"


def simplify_or_none(text):
    if text is None:
        return None
    else:
        return HanziConv.toSimplified(text)


badword_regexes = list(map(HanziConv.toSimplified, [
    r"王八蛋",  # son of a bitch
    r"他媽的",  # "his mother's"
    r"去你媽",  # "to your mother"
    r"去你的",  # "to yours"
    r"婊子", r"妓女",  # prostitute
    r"日了?狗",  # lonely dog
    r"屁眼", r"混蛋",  # asshole
    r"渾蛋",  # zh-hant of previous
    r"混帳",  # variant of above
    r"王八",  # bitch
    r"白癡",  # idiot
    r"腦殘",  # brain dead
    r"智障",  # mentally retarded
    r"婊", r"妓",  # prostitute
    r"屎",  # shit
    r"屌",  # dick
    r"妈逼",  # (this is verbal but definitely bad)
    r"艹", r"肏",  # fuck (in any context)
    r"放屁",

    # Variants (homonyms) of the use of "fuck" that use 操 ("operation") and
    # 草 ("grass"), "肏" is the actual character.  "艹" is not a real character
    # but it's used this way
    r"操你", r"草你", r"日你",  # fuck you
    r"操他", r"草他", r"日他",  # fuck his
    r"操她", r"草她", r"日她",  # fuck her

    # Discrimination (racial slurs)
    r"小日本",  # little Japanese
    r"台湾狗",  # Taiwanese dogs
    r"共产中国",  # communist Chinese
    r"流氓国家",  # rogue country
    r"人渣",  # human slag
    r"我去",  # this is verbal and bad
    r"鬼子"
]))

badwords = RegexMatches(name + ".badwords", badword_regexes, wrapping=None,
                        text_preprocess=simplify_or_none)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

# Formatted from
# https://resources.allsetlearning.com/chinese/grammar/Formal_and_informal_function_words
informal_regexes = list(map(HanziConv.toSimplified, [
    # Hello
    r"你好",  # nǐ hǎo; The standard "hello" greeting.
    r"您好",  # nín hǎo; The same "hello" greeting as above
    r"你怎么样",  # nǐ zěnmeyàng?; "What's up?", "How are you doing?"

    # Good afternoon
    r"午安",  # wǔ'an; note: seldom used in the Mainland.
    r"下午好",  # xìawǔ hǎo! Seldom used in the Republic of China

    # Good evening / Good night
    r"晚安",  # wǎn'an; Literally "Peace at night", Good night.
    r"晚上好",  # wǎnshang hǎo; Good evening!

    # Good-bye
    r"再見",  # zàijian; Literally "See you again".
    r"明天見",  # míngtian jiàn; Literally "See you tomorrow".
    r"拜拜",  # bāibāi/báibái; From English "Bye-Bye".
    r"回頭見",  # huítóujiàn: roughly equivalent to "see you soon"
    r"回見",  # huíjiàn; usually used in Beijing or written Chinese.
    r"再會",  # zàihuì: Literally "[we'll] hello again".
    r"666+", r"233+",  # No one knows why.  But this belongs
]))

informals = RegexMatches(name + ".informals", informal_regexes, wrapping=None,
                         text_preprocess=simplify_or_none)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""

words_to_watch_regexes = list(map(HanziConv.toSimplified, [
    # Advertising language
    r"本台",  # this channel
    r"本公司",  # this company
    r"代刷", r"代练", r"代抢",  # someone who plays games for you
    r"强势回归",  # "mightly" return
    r"超值",  # very cost-effective
    r"一条龙",  # a proverb? "one line of dragon"
    r"一夜情",  # selling one's body (advertising)
    r"世界一流", r"国际一流",  # world first-class
    r"用户第一", r"用户满意", r"用户至上",  # customer-first
    r"核心价值", r"核心团队", r"核心宗旨",  # core value
    r"服务小姐",  # service lady
    r"服务范围",  # service area
    r"服务项目",  # service items
    r"服务理念",  # service philosophy
]))

words_to_watch = RegexMatches(name + ".words_to_watch", words_to_watch_regexes,
                              wrapping=None,
                              text_preprocess=simplify_or_none)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
advertising language regexes.
"""
