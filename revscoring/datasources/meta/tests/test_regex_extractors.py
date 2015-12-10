from nose.tools import eq_

from ....dependencies import solve
from ...datasource import Datasource
from ..regex_extractors import SegmentRegexExtractor, TextRegexExtractor


def return_foo():
    return "foo"

segments = Datasource("segments")

text = Datasource("text")

text_extractor = TextRegexExtractor("text_extractor", text,
                                    ["foo bar", "bar foo"])

segment_extractor = SegmentRegexExtractor("text_extractor", segments,
                                          ["foo bar", "bar foo"])


def test_text_extractor():
    cache = {text: "This is some text foo bar nope bar foo"}

    eq_(solve(text_extractor, cache=cache),
        ["foo bar", "bar foo"])


def test_segment_extractor():
    cache = {segments: ["This is some text foo bar nope bar foo", "foo bar",
                        "foo"]}

    eq_(solve(segment_extractor, cache=cache),
        ["foo bar", "bar foo", "foo bar"])
