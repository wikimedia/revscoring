import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages import vietnamese

from .util import compare_extraction

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

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(vietnamese.badwords.revision.datasources.matches,
                       BAD, OTHER)

    assert vietnamese.badwords == pickle.loads(
        pickle.dumps(vietnamese.badwords))


def test_informals():
    compare_extraction(vietnamese.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    assert vietnamese.informals == pickle.loads(
        pickle.dumps(vietnamese.informals))


def test_dictionary():
    cache = {r_text: "Hóa thạch của: loài này được."}
    assert (solve(vietnamese.dictionary.revision.datasources.dict_words,
                  cache=cache) ==
            ['thạch', 'của', 'loài', 'này', 'được'])
    assert (solve(vietnamese.dictionary.revision.datasources.non_dict_words,
                  cache=cache) ==
            ['Hóa'])

    assert (vietnamese.dictionary ==
            pickle.loads(pickle.dumps(vietnamese.dictionary)))


def test_stopwords():
    cache = {r_text: "Hóa thạch của: loài này được."}
    assert (solve(vietnamese.stopwords.revision.datasources.stopwords,
                  cache=cache) ==
            ['của', 'này', 'được'])
    assert (solve(vietnamese.stopwords.revision.datasources.non_stopwords,
                  cache=cache) ==
            ['Hóa', 'thạch', 'loài'])

    assert vietnamese.stopwords == pickle.loads(
        pickle.dumps(vietnamese.stopwords))
