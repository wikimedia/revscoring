from collections import namedtuple

from nose.tools import eq_

from ..prev_misspellings import prev_misspellings


def test_prev_misspellings():
    FakeLanguage = namedtuple("Language", ['misspellings'])
    
    def misspellings(words):
        return (w for w in words if w in {"werds"})
    
    language = FakeLanguage(misspellings)
    revision_text = "This is werds. 7438 And stuff."
    
    eq_(prev_misspellings(language, revision_text), 1)
