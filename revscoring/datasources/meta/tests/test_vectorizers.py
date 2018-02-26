from unittest.mock import patch
import numpy as np

from .. import vectorizers
from revscoring.datasources import revision_oriented as ro
from revscoring.dependencies import solve
from revscoring.features import wikitext

test_vectors = {'a': np.ones(200),
                'b': np.ones(200),
                'c': np.ones(200)}

loadvectors_full_path = vectorizers.__name__ + \
    '.word2vec.load_kv'


@patch(loadvectors_full_path)
def test_vectorize(loadw2v):
    loadw2v.return_value = test_vectors
    wv = vectorizers.word2vec(wikitext.revision.datasources.tokens,
                                       'prefix', 'vector_name', dim=200)
    vector = solve(wv, cache={ro.revision.text: 'a bv c d'})
    assert len(vector) == 7
    assert len(vector[0]) == 200
