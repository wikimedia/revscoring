from collections import namedtuple

from nose.tools import eq_

from ..badwords_added import badwords_added


def test_badwords_added():
    FakeLanguage = namedtuple("Language", ['badwords'])
    
    def badwords(words):
        return (w for w in words if w in {"shit", "bitch", "palavrão"})
    
    language = FakeLanguage(badwords)
    
    eq_(badwords_added(language, ["This is shit words.", "And bitch."]), 2)
    eq_(badwords_added(language, ["Um palavrão"]), 1)
