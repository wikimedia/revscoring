from .features import RegexMatches

name = "japanese"

# Copied from https://gist.github.com/whym/b5ac3feb2a78797c9d98
# Yusuke Matsubara (CCO)
badword_regexes = [
    r"死ね",
    r"しね",
    r"シネ",
    r"あほ",
    r"アホ",
    r"ばか",
    r"バカ",
    r"やりまん",
    r"ヤリマン",
    r"まんこ",
    r"マンコ",
    r"うんこ",
    r"ウンコ",
    r"きもい",
    r"キモイ",
    r"痴女",
    r"淫乱",
    r"在日",
    r"チョン",
    r"支那",
    r"うざい",
    r"うぜー",
    r"ｗｗ+",
    r"ww+"
]

badwords = RegexMatches(name + ".badwords", badword_regexes,
                        wrapping=False)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

# Copied from https://gist.github.com/whym/b5ac3feb2a78797c9d98
# Yusuke Matsubara (CCO)
informal_regexes = [
    # Words
    r"\（笑\）",
    r"\(笑\)",
    r"・・・+",
    r"お願いします",
    r"こんにちは",
    r"はじめまして",
    r"ありがとうございます",
    r"ありがとうございました",
    r"すみません",
    r"思います",
    r"はい",
    r"いいえ",
    r"ですが",
    r"あなた",
    r"おっしゃる",
    # Patterns
    r"ね。",
    r"な。",
    r"よ。",
    r"わ。",
    r"が。",
    r"は。",
    r"に。",
    r"か？",
    r"んか。",
    r"すか。",
    r"ます。",
    r"せん。",
    r"です。",
    r"ました。",
    r"でした。",
    r"しょう。",
    r"しょうか。",
    r"ください。",
    r"下さい。",
    r"ますが",
    r"ですが",
    r"ましたが",
    r"でしたが",
    r"さん、",
    r"様、",
    r"ちゃい",
    r"ちゃう",
    r"ちゃえ",
    r"ちゃっ",
    r"っちゃ",
    r"じゃない",
    r"じゃなく"
]

informals = RegexMatches(name + ".informals", informal_regexes,
                         wrapping=False)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
