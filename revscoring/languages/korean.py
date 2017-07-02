from .features import RegexMatches

name = "korean"

# No useful dictionary.  hunspell-ko is broken on Ubuntu 14.10

# No korean stopwords

# No stemmer


badword_regexes = [
    r'ㅂㅅ',
    r'ㅅㅂ',
    r'ㅆㅂ',
    r'ㅈㄹ',
    r'간나',
    r'갈보',
    r'개(기[다지]|년|끼|소?리|수작|새끼|자식|좆|차반)',
    r'걸레년',
    r'계집년',
    r'그지새끼',
    r'꼴값',
    r'눈깔',
    r'느금마',
    r'대가리', r'대갈빡',
    r'뒈져라', r'뒤져', r'뒤져라', r'디져라',
    r'또라이',
    r'띠발',
    r'미친놈',
    r'버러지년',
    r'병시나', r'병신',
    r'븅신',
    r'빌어먹을',
    r'빙신',
    r'빡대갈',
    r'뻐큐',
    r'색히',
    r'시부랄',
    r'쌍년', r'쌍놈',
    r'썅', r'썅년', r'썅놈',
    r'쓰레기같은', r'쓰벌',
    r'씨바', r'씨발', r'씨발년', r'씨발놈',
    r'씹구멍', r'씹물', r'씹버러지', r'씹빨', r'씹새', r'씹알', r'씹창',
    r'아가리',
    r'애자',
    r'앰창', r'엠창',
    r'염병', r'옘병',
    r'잡년',
    r'조빱',
    r'존나',
    r'좆같', r'좆까', r'좆나', r'좆만한', r'좆밥', r'좆빠는', r'좆뺑이', r'좆씹',
    r'지랄',
    r'찌질이',
    r'찐따',
    r'창년',
    r'처먹다', r'쳐먹다',
    r'호로자식',
    r'화냥',
    r'후레'
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
    r"아니오"
    r"잠시만요"
    r"합니다만", r"입니다만",
    r"\w*니다", r"\w+니까",
    r"\w*세요",
    r"\w*데요",
    r"\w*지요",
    r"\w*네요",
    r"\w*어요",
    r"\w*하죠"
]

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
