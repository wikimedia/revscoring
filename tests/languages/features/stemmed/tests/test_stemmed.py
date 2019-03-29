import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages.features.stemmed.stemmed import Stemmed


def stem_word(w):
    return w[0].lower()


stemmed = Stemmed("english.stemmed", stem_word)

r_text = revision_oriented.revision.text
p_text = revision_oriented.revision.parent.text


def test_stemmed():
    cache = {p_text: "This is good.  These are words.  45 is a number",
             r_text: "This is bad.  These are still words.  50 is a number"}

    assert (solve(stemmed.revision.datasources.stems, cache=cache) ==
            ['t', 'i', 'b', 't', 'a', 's', 'w', 'i', 'a', 'n'])
    assert solve(stemmed.revision.unique_stems, cache=cache) == 7
    assert solve(stemmed.revision.stem_chars, cache=cache) == 10
    assert (solve(stemmed.revision.parent.datasources.stems, cache=cache) ==
            ['t', 'i', 'g', 't', 'a', 'w', 'i', 'a', 'n'])
    assert solve(stemmed.revision.parent.unique_stems, cache=cache) == 6
    assert solve(stemmed.revision.parent.stem_chars, cache=cache) == 9

    assert (solve(stemmed.revision.datasources.stem_frequency, cache=cache) ==
            {'t': 2, 'i': 2, 'b': 1, 'a': 2, 's': 1, 'w': 1, 'n': 1})
    assert (solve(stemmed.revision.parent.datasources.stem_frequency, cache=cache) ==
            {'t': 2, 'i': 2, 'g': 1, 'a': 2, 'w': 1, 'n': 1})

    diff = stemmed.revision.diff
    assert (solve(diff.datasources.stem_delta, cache=cache) ==
            {'b': 1, 'g': -1, 's': 1})
    assert solve(diff.stem_delta_sum, cache=cache) == 1
    assert solve(diff.stem_delta_increase, cache=cache) == 2
    assert solve(diff.stem_delta_decrease, cache=cache) == -1

    assert (solve(diff.datasources.stem_prop_delta, cache=cache) ==
            {'b': 1, 'g': -1, 's': 1})
    assert round(solve(diff.stem_prop_delta_sum, cache=cache), 2) == 1.0
    assert (round(solve(diff.stem_prop_delta_increase, cache=cache), 2) ==
            2.0)
    assert (round(solve(diff.stem_prop_delta_decrease, cache=cache), 2) ==
            -1.0)


def test_pickling():
    assert (pickle.loads(pickle.dumps(stemmed.revision.unique_stems)) ==
            stemmed.revision.unique_stems)
    assert (pickle.loads(pickle.dumps(stemmed.revision.stem_chars)) ==
            stemmed.revision.stem_chars)
    assert (pickle.loads(pickle.dumps(stemmed.revision.parent.unique_stems)) ==
            stemmed.revision.parent.unique_stems)
    assert (pickle.loads(pickle.dumps(stemmed.revision.parent.stem_chars)) ==
            stemmed.revision.parent.stem_chars)

    diff = stemmed.revision.diff
    assert (pickle.loads(pickle.dumps(diff.stem_delta_sum)) ==
            diff.stem_delta_sum)
    assert (pickle.loads(pickle.dumps(diff.stem_delta_increase)) ==
            diff.stem_delta_increase)
    assert (pickle.loads(pickle.dumps(diff.stem_delta_decrease)) ==
            diff.stem_delta_decrease)
    assert (pickle.loads(pickle.dumps(diff.stem_prop_delta_sum)) ==
            diff.stem_prop_delta_sum)
    assert (pickle.loads(pickle.dumps(diff.stem_prop_delta_increase)) ==
            diff.stem_prop_delta_increase)
    assert (pickle.loads(pickle.dumps(diff.stem_prop_delta_decrease)) ==
            diff.stem_prop_delta_decrease)
