import pickle

from hanziconv import HanziConv
from revscoring.datasources import revision_oriented
from revscoring.languages import chinese

from .util import compare_extraction

bad_init = [
    "王八蛋",  # son of a bitch
    "他媽的",  # "his mother's"
    "去你媽",  # "to your mother"
    "去你的",  # "to yours"
    "婊子", "妓女",  # prostitute
    "日狗", "日了狗",  # lonely dog
    "屁眼", "混蛋", "渾蛋",  # asshole
    "混帳",  # variant of above
    "王八",  # bitch
    "白癡",  # idiot
    "腦殘",  # brain dead
    "智障",  # mentally retarded
    "婊", "妓",  # prostitute
    "屎",  # shit
    "屌",  # dick
    "妈逼",  # (this is verbal but definitely bad)
    "艹", "肏",  # fuck (in any context)
    "放屁",  # fart

    # Variants (homonyms) of the use of "fuck" that use 操 ("operation") and
    # 草 ("grass"), "肏" is the actual character.  "艹" is not a real character
    # but it's used this way
    "操你", "草你", "日你",  # fuck you
    "操他", "草他", "日他",  # fuck his
    "操她", "草她", "日她",  # fuck her

    # Discrimination (racial slurs)
    "小日本",  # little Japanese
    "台湾狗",  # Taiwanese dogs
    "共产中国",  # communist Chinese
    "流氓国家",  # rogue country
    "人渣",  # human slag
    "我去",  # this is verbal and bad
    "鬼子"  # devil, usually a suffix
]
BAD = [HanziConv.toSimplified(word) for word in bad_init] + \
      [HanziConv.toTraditional(word) for word in bad_init]

INFORMAL = [
    # Hello
    "你好",  # nǐ hǎo; The standard "hello" greeting.
    "您好",  # nín hǎo; The same "hello" greeting as above
    "你怎么样",  # nǐ zěnmeyàng?; "What's up?", "How are you doing?"

    # Good afternoon
    "午安",  # wǔ'an; note: seldom used in the Mainland.
    "下午好",  # xìawǔ hǎo! Seldom used in the Republic of China

    # Good evening / Good night
    "晚安",  # wǎn'an; Literally "Peace at night", Good night.
    "晚上好",  # wǎnshang hǎo; Good evening!

    # Good-bye
    "再見",  # zàijian; Literally "See you again".
    "明天見",  # míngtian jiàn; Literally "See you tomorrow".
    "拜拜",  # bāibāi/báibái; From English "Bye-Bye".
    "回頭見",  # huítóujiàn: roughly equivalent to "see you soon"
    "回見",  # huíjiàn; usually used in Beijing or written Chinese.
    "再會",  # zàihuì: Literally "[we'll] hello again".
    "66666666", "666",
    "233", "2333333"
]

WORDS_TO_WATCH = [
    # Advertising language
    "本台",  # this channel
    "本公司",  # this company
    "代刷", "代练", "代抢",  # someone who plays games for you
    "强势回归",  # "mightly" return
    "超值",  # very cost-effective
    "一条龙",  # a proverb? "one line of dragon"
    "一夜情",  # selling one's body (advertising)
    "世界一流", "国际一流",  # world first-class
    "用户第一", "用户满意", "用户至上",  # customer-first
    "核心价值", "核心团队", "核心宗旨",  # core value
    "服务小姐",  # service lady
    "服务范围",  # service area
    "服务项目",  # service items
    "服务理念",  # service philosophy
]

OTHER = [
    """2005年大西洋颶風季是有纪录以来最活跃的大西洋颶風季，至今仍保持着多项纪录。
    全季对大范围地区造成毁灭性打击，共导致3,913人死亡，损失数额更创下新纪录，高达1592亿美元。
    本季单大型飓风就有7场之多，其中5场在登陆时仍有大型飓风强度，分别是颶風丹尼斯、艾米莉、
    卡特里娜、丽塔和威尔玛，大部分人员伤亡和财产损失都是这5场飓风引起。
    墨西哥的金塔納羅奧州和尤卡坦州，
    以及美国的佛罗里达州和路易斯安那州都曾两度受大型飓风袭击；古巴、巴哈马、海地，
    美国的密西西比州和得克萨斯州，还有墨西哥的塔毛利帕斯州都曾直接受1场大型飓风冲击，
    还有至少1场在附近掠过。美國墨西哥灣沿岸地區是本季受灾最严重的所在，
    飓风卡特里娜产生高达10米的风暴潮，引发毁灭性洪灾，密西西比州沿海地区的大部分建筑物被毁，
    风暴之后又令新奥尔良防洪堤决口，整个城市因此受到重创。此外，飓风斯坦同溫帶氣旋共同影响，
    在中美洲多地引发致命的泥石流，其中又以危地马拉灾情最为严重。"""
]

r_text = revision_oriented.revision.text


def simplified_eq(a, b):
    return len(a) == len(b) and \
           HanziConv.toSimplified(a[0]) == \
           HanziConv.toSimplified(b[0])


def test_badwords():
    compare_extraction(chinese.badwords.revision.datasources.matches,
                       BAD, OTHER, eq=simplified_eq)
    assert chinese.badwords == pickle.loads(pickle.dumps(chinese.badwords))


def test_informals():
    compare_extraction(chinese.informals.revision.datasources.matches,
                       INFORMAL, OTHER, eq=simplified_eq)

    assert chinese.informals == pickle.loads(pickle.dumps(chinese.informals))


def test_words_to_watch():
    compare_extraction(chinese.words_to_watch.revision.datasources.matches,
                       WORDS_TO_WATCH, OTHER, eq=simplified_eq)

    assert chinese.words_to_watch == \
           pickle.loads(pickle.dumps(chinese.words_to_watch))
