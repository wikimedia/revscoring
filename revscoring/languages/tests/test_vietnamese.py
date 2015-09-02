import pickle

from nose.tools import eq_

from .. import vietnamese
from ...datasources import revision
from ...dependencies import solve

BAD = [
    "đít", "địt",
    "dâm", "dzâm", "giâm",
    "cu", "ku",
    "cứt",
    "lôn", "lồn",
    "đụ", "đù",
    "đái",
    "đéo",
    "đĩ",
    "ỉa",
    "cặt", "cặc", "kặt", "kặc"
]

INFORMAL = [
    "bợn",
    "chớ", "chứ",
    "chẳng",
    "cú",
    "fải",
    "khỉ",
    "mày",
    "nghịch",
    "ngu",
    "nguỵ",
    "ngụy",
    "quái",
    "thôi",
    "thằng",
    "tui",
    "vời",
    "wái",
    "zì",
    "đừng",
    "ơi",
    "ừ",
]

OTHER = [
    """
    Acrocanthosaurus là một chi khủng long chân thú từng tồn tại ở khu vực
    ngày nay là Bắc Mỹ vào tầng Apt và giai đoạn đầu của tầng Alba thuộc kỷ
    Phấn trắng. Giống như hầu hết các chi khủng long khác, Acrocanthosaurus
    chỉ có một loài duy nhất: A. atokensis. Hóa thạch của loài này được tìm
    thấy chủ yếu ở các tiểu bang Hoa Kỳ Oklahoma, Texas và Wyoming, mặc dù
    răng nó đã được tìm thấy xa về phía đông tận Maryland. Acrocanthosaurus
    là động vật ăn thịt hai chân. Nó được biết đến với những gai thần kinh
    cao trên các đốt sống, mà rất có thể được dùng để nâng đỡ một dãy bướu
    thịt trên lưng, cổ và hông.
    """
]


def compare_extraction(extractor, examples, counter_examples):

    for example in examples:
        eq_(extractor.process(example), [example])
        eq_(extractor.process("Sentence " + example + " sandwich."), [example])
        eq_(extractor.process("Sentence end " + example + "."), [example])
        eq_(extractor.process(example + " start of sentence."), [example])

    for example in counter_examples:
        eq_(extractor.process(example), [])
        eq_(extractor.process("Sentence " + example + " sandwich."), [])
        eq_(extractor.process("Sentence end " + example + "."), [])
        eq_(extractor.process(example + " start of sentence."), [])


def test_badwords():
    compare_extraction(vietnamese.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(vietnamese.revision.informals_list, INFORMAL, OTHER)


def test_revision():
    # Words
    cache = {revision.text: "Hóa thạch của: loài này được."}
    eq_(solve(vietnamese.revision.words_list, cache=cache),
        ["Hóa", "thạch", "của", "loài", "này", "được"])

    # Misspellings
    cache = {revision.text: 'mà rất có thể được worngly. <td>'}
    eq_(solve(vietnamese.revision.misspellings_list, cache=cache), ["worngly"])


def test_presence():
    assert hasattr(vietnamese.revision, "words")
    assert hasattr(vietnamese.revision, "content_words")
    assert hasattr(vietnamese.revision, "badwords")
    assert hasattr(vietnamese.revision, "informals")
    assert hasattr(vietnamese.revision, "misspellings")

    assert hasattr(vietnamese.parent_revision, "words")
    assert hasattr(vietnamese.parent_revision, "content_words")
    assert hasattr(vietnamese.parent_revision, "badwords")
    assert hasattr(vietnamese.parent_revision, "informals")
    assert hasattr(vietnamese.parent_revision, "misspellings")

    assert hasattr(vietnamese.diff, "words_added")
    assert hasattr(vietnamese.diff, "badwords_added")
    assert hasattr(vietnamese.diff, "informals_added")
    assert hasattr(vietnamese.diff, "misspellings_added")
    assert hasattr(vietnamese.diff, "words_removed")
    assert hasattr(vietnamese.diff, "badwords_removed")
    assert hasattr(vietnamese.diff, "informals_removed")
    assert hasattr(vietnamese.diff, "misspellings_removed")


def test_pickling():

    eq_(vietnamese, pickle.loads(pickle.dumps(vietnamese)))
