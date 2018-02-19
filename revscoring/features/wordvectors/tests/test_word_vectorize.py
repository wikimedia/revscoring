from unittest.mock import patch
import numpy as np

from .. import word_vectorizers
from ....datasources import revision_oriented as ro
from ....dependencies import solve
from revscoring.features import wikitext

test_vectors = {'a': np.ones(200),
                'b': np.ones(200),
                'c': np.ones(200)}

loadvectors_full_path = word_vectorizers.__name__ + \
    '.word_vectors.load_word2vec'


@patch(loadvectors_full_path)
def test_vectorize(loadw2v):
    loadw2v.return_value = test_vectors
    wv = word_vectorizers.word_vectors(wikitext.revision.datasources.tokens,
                                       'prefix', 'vector_name', dim=200)
    vector = solve(wv, cache={ro.revision.text: 'a bv c d'})
    assert int(round(vector[0], 2) * 100) / 100 == 0.28
