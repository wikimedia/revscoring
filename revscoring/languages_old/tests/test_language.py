import pickle

from nose.tools import assert_not_equal, eq_, raises

from ...dependencies import solve
from ...dependencies.errors import DependencyError
from ..language import Language, LanguageUtility, is_badword, is_stopword


def process_is_badword():
    def is_badword(word):
        return word == "badword"
    return is_badword

my_is_badword = LanguageUtility("is_badword", process_is_badword)

def test_language_utility():
    eq_(is_badword == is_badword, True)
    eq_(is_badword != is_badword, False)


def test_language():

    l = Language('revscoring.languages.test', [my_is_badword])

    assert is_badword in l.context
    eq_(l.context[is_badword]()("badword"), True)

    recovered_l = pickle.loads(pickle.dumps(l))
    eq_(recovered_l, l)
    eq_(l == 5678, False)
    eq_(l != 5678, True)
    recovered_context = recovered_l.context

    assert is_badword in recovered_context
    eq_(recovered_context[is_badword]()("badword"), True)

@raises(DependencyError)
def test_not_implemented():

    l = Language('revscoring.languages.test', [])
    solve(is_stopword, context=l.context)

def test_from_config_module():
    config = {
        'languages': {
            'english': {
                'module': "revscoring.languages.english"
            }
        }
    }

    english = Language.from_config(config, 'english')
    english.solve(is_badword)

@raises(RuntimeError)
def test_from_config_class():
    config = {
        'languages': {
            'english': {
                'class': "revscoring.languages.Language",
                'param': "Some param"
            }
        }
    }

    english = Language.from_config(config, 'english')
