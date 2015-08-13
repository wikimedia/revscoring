import pickle

from nose.tools import eq_

from .. import hebrew, language
from ...datasources import diff, parent_revision, revision
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
    cache = {revision.text: "סוויפט גדלה בוויומיסינג, פנסילבניה, ועברה לנאשוויל"}
    eq_(solve(hebrew.revision.words_list, cache=cache),
        ["סוויפט" ,"גדלה" ,"בוויומיסינג" ,"פנסילבניה" ,"ועברה" ,"לנאשוויל"])

    # Misspellings
    cache = {revision.text: 'בגלל חטול <td>'}
    eq_(solve(hebrew.revision.misspellings_list, cache=cache), ["חטול"])
