
from .. import vectorizers
from revscoring.datasources import revision_oriented as ro
from revscoring.dependencies import solve
from revscoring.features import wikitext

test_vectors = {'a': [1] * 200,
                'b': [1] * 200,
                'c': [1] * 200}


def test_vectorize():
    wv = vectorizers.word2vec(wikitext.revision.datasources.tokens,
                              test_vectors, dim=200, name='word vectors')
    vector = solve(wv, cache={ro.revision.text: 'a bv c d'})
    assert len(vector) == 7
    assert len(vector[0]) == 200
