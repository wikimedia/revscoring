from collections import namedtuple

from nose.tools import eq_

from ..prev_badwords import prev_badwords


def test_prev_badwords():
    FakeLanguage = namedtuple("Language", ['badwords'])
    
    def badwords(words):
        return (w for w in words if w in {"badword", "bad", "word"})
    
    language = FakeLanguage(badwords)
    revision_text = "This is word. 7438 And stuff."
    eq_(prev_badwords(language, revision_text), 1)

    revision_text = "Texto com bad badword digtiação."
    eq_(prev_badwords(language, revision_text), 2)
