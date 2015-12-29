import pickle

from nose.tools import eq_

from ....dependencies import solve
from ...datasource import Datasource
from ..extractors import regextract


def return_foo():
    return "foo"

segments = Datasource("segments")

text = Datasource("text")

text_extractor = regextract(["foo bar", "bar foo"], text,
                            name="text_extractor")

segment_extractor = regextract(["foo bar", "bar foo"], segments,
                               name="text_extractor")


def test_text_extractor():
    cache = {text: "This is some text foo bar nope bar foo"}

    eq_(solve(text_extractor, cache=cache),
        ["foo bar", "bar foo"])

    eq_(pickle.loads(pickle.dumps(text_extractor)), text_extractor)


def test_segment_extractor():
    cache = {segments: ["This is some text foo bar nope bar foo", "foo bar",
                        "foo"]}

    eq_(solve(segment_extractor, cache=cache),
        ["foo bar", "bar foo", "foo bar"])

    eq_(pickle.loads(pickle.dumps(segment_extractor)), segment_extractor)
