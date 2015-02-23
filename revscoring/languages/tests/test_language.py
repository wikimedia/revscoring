import pickle

from nose.tools import eq_

from ..language import Language, LanguageUtility


def process_is_badword():
    def is_badword(word):
        return word == "badword"
    return is_badword

is_badword = LanguageUtility("is_badword", process_is_badword)

def test_language():
    
    l = Language('revscoring.languages.test', [is_badword])
    
    cache = l.cache()
    assert is_badword in cache
    eq_(cache[is_badword]("badword"), True)
    
    recovered_l = pickle.loads(pickle.dumps(l))
    recovered_cache = recovered_l.cache()
    
    print(hash(is_badword) == hash(recovered_l.utilities[0]))
    
    assert is_badword in recovered_cache
    eq_(recovered_cache[is_badword]("badword"), True)
