import pickle

from nose.tools import assert_not_equal, eq_, raises

from ...dependent import DependencyError, solve
from ..language import Language, LanguageUtility, is_stopword


def process_is_badword():
    def is_badword(word):
        return word == "badword"
    return is_badword

is_badword = LanguageUtility("is_badword", process_is_badword)

def test_language_utility():
    eq_(is_badword == is_badword, True)
    eq_(is_badword != is_badword, False)


def test_language():

    l = Language('revscoring.languages.test', [is_badword])

    cache = l.cache()
    assert is_badword in cache
    eq_(cache[is_badword]("badword"), True)

    recovered_l = pickle.loads(pickle.dumps(l))
    eq_(recovered_l, l)
    eq_(l == 5678, False)
    eq_(l != 5678, True)
    recovered_cache = recovered_l.cache()

    print(hash(is_badword) == hash(recovered_l.utilities[0]))

    assert is_badword in recovered_cache
    eq_(recovered_cache[is_badword]("badword"), True)

@raises(DependencyError)
def test_not_implemented():

    l = Language('revscoring.languages.test', [])
    solve(is_stopword, cache=l.cache())
