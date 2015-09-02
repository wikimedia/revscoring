import pickle

from nose.tools import eq_

from .. import hebrew
from ...datasources import revision
from ...dependencies import solve

BAD = [
    "שרמוטה"
]

INFORMAL = [
    "בגללך"  # Because of you
]

OTHER = [
    "בגלל", "חתול"
]


def compare_extraction(extractor, examples, counter_examples):

    for example in examples:
        eq_(extractor.process(example), [example])
        eq_(extractor.process("Sentence " + example + " sandwich."), [example])
        eq_(extractor.process("Sentence end " + example + "."), [example])
        eq_(extractor.process(example + " start of sentence."), [example])

    for example in counter_examples:
        eq_(extractor.process(example), [])
        eq_(extractor.process("Sentence " + example + " sandwich."), [])
        eq_(extractor.process("Sentence end " + example + "."), [])
        eq_(extractor.process(example + " start of sentence."), [])


def test_badwords():
    compare_extraction(hebrew.revision.badwords_list, BAD, OTHER)


def test_informals():
    compare_extraction(hebrew.revision.informals_list, INFORMAL, OTHER)


def test_revision():
    # Words
    cache = {revision.text: "סוויפט גדלה בוויומיסינג, פנסילבניה, לנאשוויל"}
    eq_(solve(hebrew.revision.words_list, cache=cache),
        ["סוויפט", "גדלה", "בוויומיסינג", "פנסילבניה", "לנאשוויל"])

    # Misspellings
    cache = {revision.text: 'בגלל חטול <td>'}
    eq_(solve(hebrew.revision.misspellings_list, cache=cache), ["חטול"])


def test_presence():
    assert hasattr(hebrew.revision, "words")
    assert hasattr(hebrew.revision, "content_words")
    assert hasattr(hebrew.revision, "badwords")
    assert hasattr(hebrew.revision, "informals")
    assert hasattr(hebrew.revision, "misspellings")

    assert hasattr(hebrew.parent_revision, "words")
    assert hasattr(hebrew.parent_revision, "content_words")
    assert hasattr(hebrew.parent_revision, "badwords")
    assert hasattr(hebrew.parent_revision, "informals")
    assert hasattr(hebrew.parent_revision, "misspellings")

    assert hasattr(hebrew.diff, "words_added")
    assert hasattr(hebrew.diff, "badwords_added")
    assert hasattr(hebrew.diff, "informals_added")
    assert hasattr(hebrew.diff, "misspellings_added")
    assert hasattr(hebrew.diff, "words_removed")
    assert hasattr(hebrew.diff, "badwords_removed")
    assert hasattr(hebrew.diff, "informals_removed")
    assert hasattr(hebrew.diff, "misspellings_removed")


def test_pickling():

    eq_(hebrew, pickle.loads(pickle.dumps(hebrew)))
