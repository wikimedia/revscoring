import pickle

from nose.tools import eq_

from .. import japanese
from .util import compare_extraction

BAD = [
    "死ね",
    "しね",
    "シネ",
    "あほ",
    "アホ",
    "ばか",
    "バカ",
    "やりまん",
    "ヤリマン",
    "まんこ",
    "マンコ",
    "うんこ",
    "ウンコ",
    "きもい",
    "キモイ",
    "痴女",
    "淫乱",
    "在日",
    "チョン",
    "支那",
    "うざい",
    "うぜー",
    "ｗｗｗｗ",
    "wwww",
    "ｗｗｗｗｗｗｗｗ",
    "wwwwwwwwwwwwwww"
]

INFORMAL = [
    # Words
    "（笑）",
    "(笑)",
    "・・・",
    "お願いします",
    "こんにちは",
    "はじめまして",
    "ありがとうございます",
    "ありがとうございました",
    "すみません",
    "思います",
    "はい",
    "いいえ",
    "ですが",
    "あなた",
    "おっしゃる",

    # sub-word patterns
    "ね。",
    "な。",
    "よ。",
    "わ。",
    "が。",
    "は。",
    "に。",
    "か？",
    "んか。",
    "すか。",
    "ます。",
    "せん。",
    "です。",
    "ました。",
    "でした。",
    "しょう。",
    "しょうか。",
    "ください。",
    "下さい。",
    "ますが",
    "ですが",
    "ましたが",
    "でしたが",
    "さん、",
    "様、",
    "ちゃい",
    "ちゃう",
    "ちゃえ",
    "ちゃっ",
    "っちゃ",
    "じゃない",
    "じゃなく"
]

OTHER = [
    """
    本項で解説する地方病とは、山梨県における日本住血吸虫症の呼称であり、
    長い間その原因が明らかにならず住民を苦しめた感染症である。ここでは、
    その克服・撲滅に至る歴史について説明する。
    この疾患は住血吸虫類に分類される寄生虫である日本住血吸虫の寄生によって発症する寄生虫病であり、
    ヒトを含む哺乳類全般の血管内部に寄生感染する人獣共通感染症でもある。

    病名および原虫に日本の国名が冠されているのは、
    疾患の原因となる病原体（日本住血吸虫）の生体が、
    世界で最初に日本国内（現：山梨県甲府市）で発見されたことによるものであって、
    日本固有の疾患というわけではない。日本住血吸虫症は、中国、フィリピン、
    インドネシアの3カ国を中心に、
    年間数千人から数万人規模の新規感染患者が発生しており、
    世界保健機関　(WHO)などによって、さまざまな対策が行われている。
    """
]


def test_badwords():
    compare_extraction(japanese.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(japanese.badwords, pickle.loads(pickle.dumps(japanese.badwords)))


def test_informals():
    compare_extraction(japanese.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(japanese.informals, pickle.loads(pickle.dumps(japanese.informals)))
