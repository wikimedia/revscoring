import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.features.wikitext import revision

r_text = revision_oriented.revision.text
p_text = revision_oriented.revision.parent.text


def test_chars():
    cache = {p_text: "This is some nice text.",
             r_text: "This is some more text."}

    assert solve(revision.chars, cache=cache) == 23
    assert solve(revision.parent.chars, cache=cache) == 23
    assert solve(revision.diff.chars_added, cache=cache) == 4
    assert solve(revision.diff.chars_removed, cache=cache) == 4

    assert pickle.loads(pickle.dumps(revision.chars)) == revision.chars
    assert (pickle.loads(pickle.dumps(revision.parent.chars)) ==
            revision.parent.chars)
    assert (pickle.loads(pickle.dumps(revision.diff.chars_added)) ==
            revision.diff.chars_added)
    assert (pickle.loads(pickle.dumps(revision.diff.chars_removed)) ==
            revision.diff.chars_removed)


def test_numeric_chars():
    cache = {p_text: "This is some 45 nice text.",
             r_text: "This is some more 5000 text."}

    assert solve(revision.numeric_chars, cache=cache) == 4
    assert solve(revision.parent.numeric_chars, cache=cache) == 2
    assert solve(revision.diff.numeric_chars_added, cache=cache) == 4
    assert solve(revision.diff.numeric_chars_removed, cache=cache) == 2

    assert (pickle.loads(pickle.dumps(revision.numeric_chars)) ==
            revision.numeric_chars)
    assert (pickle.loads(pickle.dumps(revision.parent.numeric_chars)) ==
            revision.parent.numeric_chars)
    assert (pickle.loads(pickle.dumps(revision.diff.numeric_chars_added)) ==
            revision.diff.numeric_chars_added)
    assert (pickle.loads(pickle.dumps(revision.diff.numeric_chars_removed)) ==
            revision.diff.numeric_chars_removed)


def test_whitespace_chars():
    cache = {p_text: "This is some\tnice text.",
             r_text: "This is some\nmore\ntext."}

    assert solve(revision.whitespace_chars, cache=cache) == 4
    assert solve(revision.parent.whitespace_chars, cache=cache) == 4
    assert solve(revision.diff.whitespace_chars_added, cache=cache) == 2
    assert solve(revision.diff.whitespace_chars_removed, cache=cache) == 2

    assert (pickle.loads(pickle.dumps(revision.whitespace_chars)) ==
            revision.whitespace_chars)
    assert (pickle.loads(pickle.dumps(revision.parent.whitespace_chars)) ==
            revision.parent.whitespace_chars)
    assert (pickle.loads(pickle.dumps(revision.diff.whitespace_chars_added)) ==
            revision.diff.whitespace_chars_added)
    assert (pickle.loads(pickle.dumps(revision.diff.whitespace_chars_removed)) ==
            revision.diff.whitespace_chars_removed)


def test_markup_chars():
    cache = {p_text: "This is some {{nice}} text.",
             r_text: "This is [[some|more]] text."}

    assert solve(revision.markup_chars, cache=cache) == 4
    assert solve(revision.parent.markup_chars, cache=cache) == 4
    assert solve(revision.diff.markup_chars_added, cache=cache) == 4
    assert solve(revision.diff.markup_chars_removed, cache=cache) == 4

    assert (pickle.loads(pickle.dumps(revision.markup_chars)) ==
            revision.markup_chars)
    assert (pickle.loads(pickle.dumps(revision.parent.markup_chars)) ==
            revision.parent.whitespace_chars)
    assert (pickle.loads(pickle.dumps(revision.diff.markup_chars_added)) ==
            revision.diff.markup_chars_added)
    assert (pickle.loads(pickle.dumps(revision.diff.markup_chars_removed)) ==
            revision.diff.markup_chars_removed)


def test_cjk_chars():
    cache = {p_text: "This is 55 {{るは}} a string.",
             r_text: "This is 56 [[壌のは]] a string."}

    assert solve(revision.cjk_chars, cache=cache) == 3
    assert solve(revision.parent.cjk_chars, cache=cache) == 2
    assert solve(revision.diff.cjk_chars_added, cache=cache) == 2
    assert solve(revision.diff.cjk_chars_removed, cache=cache) == 1

    assert (pickle.loads(pickle.dumps(revision.cjk_chars)) ==
            revision.cjk_chars)
    assert (pickle.loads(pickle.dumps(revision.parent.cjk_chars)) ==
            revision.parent.cjk_chars)
    assert (pickle.loads(pickle.dumps(revision.diff.cjk_chars_added)) ==
            revision.diff.cjk_chars_added)
    assert (pickle.loads(pickle.dumps(revision.diff.cjk_chars_removed)) ==
            revision.diff.cjk_chars_removed)


def test_entity_chars():
    cache = {p_text: "This is &nsbp; not a string.",
             r_text: "This is &middot; too a string."}

    assert solve(revision.entity_chars, cache=cache) == 8
    assert solve(revision.parent.entity_chars, cache=cache) == 6
    assert solve(revision.diff.entity_chars_added, cache=cache) == 8
    assert solve(revision.diff.entity_chars_removed, cache=cache) == 6

    assert (pickle.loads(pickle.dumps(revision.entity_chars)) ==
            revision.entity_chars)
    assert (pickle.loads(pickle.dumps(revision.parent.entity_chars)) ==
            revision.parent.entity_chars)
    assert (pickle.loads(pickle.dumps(revision.diff.entity_chars_added)) ==
            revision.diff.entity_chars_added)
    assert (pickle.loads(pickle.dumps(revision.diff.entity_chars_removed)) ==
            revision.diff.entity_chars_removed)


def test_url_chars():
    cache = {p_text: "This is https://google.com not a string.",
             r_text: "This //google.com mailto:aaron@bar.com string."}

    assert solve(revision.url_chars, cache=cache) == 32
    assert solve(revision.parent.url_chars, cache=cache) == 18
    assert solve(revision.diff.url_chars_added, cache=cache) == 32
    assert solve(revision.diff.url_chars_removed, cache=cache) == 18

    assert (pickle.loads(pickle.dumps(revision.url_chars)) ==
            revision.url_chars)
    assert (pickle.loads(pickle.dumps(revision.parent.url_chars)) ==
            revision.parent.url_chars)
    assert (pickle.loads(pickle.dumps(revision.diff.url_chars_added)) ==
            revision.diff.url_chars_added)
    assert (pickle.loads(pickle.dumps(revision.diff.url_chars_removed)) ==
            revision.diff.url_chars_removed)


def test_word_chars():
    cache = {p_text: "This is 55 not string.",
             r_text: "This is 56 too a string."}

    assert solve(revision.word_chars, cache=cache) == 16
    assert solve(revision.parent.word_chars, cache=cache) == 15
    assert solve(revision.diff.word_chars_added, cache=cache) == 4
    assert solve(revision.diff.word_chars_removed, cache=cache) == 3

    assert (pickle.loads(pickle.dumps(revision.word_chars)) ==
            revision.word_chars)
    assert (pickle.loads(pickle.dumps(revision.parent.word_chars)) ==
            revision.parent.word_chars)
    assert (pickle.loads(pickle.dumps(revision.diff.word_chars_added)) ==
            revision.diff.word_chars_added)
    assert (pickle.loads(pickle.dumps(revision.diff.word_chars_removed)) ==
            revision.diff.word_chars_removed)


def test_uppercase_word_chars():
    cache = {p_text: "This is 55 NOT string.",
             r_text: "This IS 56 TOO a string."}

    assert solve(revision.uppercase_word_chars, cache=cache) == 5
    assert solve(revision.parent.uppercase_word_chars, cache=cache) == 3
    assert solve(revision.diff.uppercase_word_chars_added, cache=cache) == 5
    assert solve(revision.diff.uppercase_word_chars_removed, cache=cache) == 3

    assert (pickle.loads(pickle.dumps(revision.uppercase_word_chars)) ==
            revision.uppercase_word_chars)
    assert (pickle.loads(pickle.dumps(revision.parent.uppercase_word_chars)) ==
            revision.parent.uppercase_word_chars)
    assert (pickle.loads(pickle.dumps(revision.diff.uppercase_word_chars_added)) ==
            revision.diff.uppercase_word_chars_added)
    assert (pickle.loads(pickle.dumps(revision.diff.uppercase_word_chars_removed)) ==
            revision.diff.uppercase_word_chars_removed)


def test_punctuation_chars():
    cache = {p_text: "This is, 55 NOT string.",
             r_text: "This IS 56 TOO a string."}

    assert solve(revision.punctuation_chars, cache=cache) == 1
    assert solve(revision.parent.punctuation_chars, cache=cache) == 2
    assert solve(revision.diff.punctuation_chars_added, cache=cache) == 0
    assert solve(revision.diff.punctuation_chars_removed, cache=cache) == 1

    assert (pickle.loads(pickle.dumps(revision.punctuation_chars)) ==
            revision.punctuation_chars)
    assert (pickle.loads(pickle.dumps(revision.parent.punctuation_chars)) ==
            revision.parent.punctuation_chars)
    assert (pickle.loads(pickle.dumps(revision.diff.punctuation_chars_added)) ==
            revision.diff.punctuation_chars_added)
    assert (pickle.loads(pickle.dumps(revision.diff.punctuation_chars_removed)) ==
            revision.diff.punctuation_chars_removed)


def test_break_chars():
    cache = {p_text: "This is, 55\n\nNOT\n\nstring.",
             r_text: "This IS 56 TOO\n\na string."}

    assert solve(revision.break_chars, cache=cache) == 2
    assert solve(revision.parent.break_chars, cache=cache) == 4
    assert solve(revision.diff.break_chars_added, cache=cache) == 0
    assert solve(revision.diff.break_chars_removed, cache=cache) == 2

    assert (pickle.loads(pickle.dumps(revision.break_chars)) ==
            revision.break_chars)
    assert (pickle.loads(pickle.dumps(revision.parent.break_chars)) ==
            revision.parent.break_chars)
    assert (pickle.loads(pickle.dumps(revision.diff.break_chars_added)) ==
            revision.diff.break_chars_added)
    assert (pickle.loads(pickle.dumps(revision.diff.break_chars_removed)) ==
            revision.diff.break_chars_removed)


def test_longest_repeated_char():
    cache = {p_text: "This is words.",
             r_text: "This is aaaa words. kkkkkkkkkkkk"}

    # Test an addition of a very long repeated char
    assert solve(revision.longest_repeated_char, cache=cache) == 12
    assert solve(revision.parent.longest_repeated_char, cache=cache) == 1
    assert solve(revision.diff.longest_repeated_char_added, cache=cache) == 12

    # Test the no-change case
    cache = {p_text: "This is words.",
             r_text: "This is words."}
    assert solve(revision.diff.longest_repeated_char_added, cache=cache) == 1

    # Test no parent case
    cache = {p_text: None}
    assert solve(revision.parent.longest_repeated_char, cache=cache) == 1

    assert (pickle.loads(pickle.dumps(revision.longest_repeated_char)) ==
            revision.longest_repeated_char)
    assert (pickle.loads(pickle.dumps(revision.parent.longest_repeated_char)) ==
            revision.parent.longest_repeated_char)
    assert (pickle.loads(pickle.dumps(revision.diff.longest_repeated_char_added)) ==
            revision.diff.longest_repeated_char_added)
