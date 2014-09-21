from collections import namedtuple

from nose.tools import eq_

from ..misspellings_added import misspellings_added


def test_misspellings_added():
    FakeLanguage = namedtuple("Language", ['misspellings'])
    
    def misspellings(words):
        return (w for w in words if w in {"werds"})
    
    language = FakeLanguage(misspellings)
    contiguous_segments_added = ["This is werds. 7438", "And stuff."]
    eq_(misspellings_added(language, contiguous_segments_added), 1)
