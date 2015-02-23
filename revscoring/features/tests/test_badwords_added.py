from nose.tools import eq_

from ..badwords_added import badwords_added


def test_badwords_added():
    def is_badword(w): return w in {"bitch", "shit", "palavrão"}
    
    eq_(badwords_added(is_badword, ["This is shit words.", "And bitch."]), 2)
    eq_(badwords_added(is_badword, ["Um palavrão"]), 1)
