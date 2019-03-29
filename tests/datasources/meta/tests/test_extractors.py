import pickle

from revscoring.datasources.datasource import Datasource
from revscoring.datasources.meta import extractors
from revscoring.dependencies import solve


def return_foo():
    return "foo"


segments = Datasource("segments")

text = Datasource("text")

text_extractor = extractors.regex(["foo bar", "bar foo"], text,
                                  name="text_extractor")

exclusion_text_extractor = extractors.regex(["foo+"], text,
                                            name="text_extractor",
                                            exclusions=['foooo'])

segment_extractor = extractors.regex(["foo bar", "bar foo"], segments,
                                     name="text_extractor")


def test_text_extractor():
    cache = {text: "This is some text foo bar nope bar foo"}
    assert solve(text_extractor, cache=cache) == ["foo bar", "bar foo"]
    cache = {text: None}
    assert solve(text_extractor, cache=cache) == []

    assert pickle.loads(pickle.dumps(text_extractor)) == text_extractor


def test_exclusion_text_extractor():
    cache = {text: "This is some text foooo bar nope bar foo fooo"}
    assert solve(exclusion_text_extractor, cache=cache) == ["foo", "fooo"]

    assert (pickle.loads(pickle.dumps(exclusion_text_extractor)) ==
            exclusion_text_extractor)


def test_segment_extractor():
    cache = {segments: ["This is some text foo bar nope bar foo", "foo bar",
                        "foo"]}
    assert (solve(segment_extractor, cache=cache) ==
            ["foo bar", "bar foo", "foo bar"])

    assert pickle.loads(pickle.dumps(segment_extractor)) == segment_extractor
