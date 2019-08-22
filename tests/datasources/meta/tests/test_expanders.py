import pickle

from revscoring import Datasource, Feature
from revscoring.datasources.meta import expanders
from revscoring.dependencies import solve


def process_chars(text):
    return len(text)

text = Datasource("text")
chars = Feature("chars", process_chars, returns=int, depends_on=[text])
many_texts = expanders.list_of(text)
many_chars = expanders.list_of(chars, depends_on=[many_texts])


def test_list_of():
    assert solve(many_chars, cache={many_texts: ["foo", "barbaz"]}) == \
           [3, 6]

    assert pickle.loads(pickle.dumps(many_chars)) == many_chars
