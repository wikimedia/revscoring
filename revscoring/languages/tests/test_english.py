import pickle

from nose.tools import eq_

from .. import english, language
from .util import all_false, all_true


def test_language():

    stem_word = english.solve(language.stem_word)

    eq_(stem_word("shitting"), "shit")
    eq_(stem_word("Shitting"), "shit")


    is_badword = english.solve(language.is_badword)

    all_true(is_badword, ["shit", "shitty", "shitting", "shitfucker",
                          "pieceofshit", "SHIT", "SHITTING",
                          "fuuckers", "motherfucker", "FUCKYOU!",
                          "whoreface", "stupid", "bitchass",
                          "japinjun"])
    all_false(is_badword, ["mother", "association", "shihtzu", "horrendous"])

    is_informal_word = english.solve(language.is_informal_word)

    all_true(is_informal_word, ["kewlest", "won't", "cant", "I", "awesome"])
    all_false(is_informal_word, ["hat", "Island", "pants", "cantelope"])

    is_misspelled = english.solve(language.is_misspelled)

    assert is_misspelled("wjwkjb")
    assert not is_misspelled("waffles")
    assert not is_misspelled("Waffles")

    is_stopword = english.solve(language.is_stopword)

    assert is_stopword("A")
    assert is_stopword("in")
    assert is_stopword("about")
    assert not is_stopword("waffles")

    pickled_english = pickle.loads(pickle.dumps(english))
    eq_(pickled_english, english)
