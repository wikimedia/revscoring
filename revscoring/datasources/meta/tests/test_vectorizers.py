
from revscoring.datasources import revision_oriented as ro
from revscoring.dependencies import solve
from revscoring.features import wikitext

from .. import vectorizers

test_vectors = {'a': [1] * 300,
                'b': [1] * 300,
                'c': [1] * 300}


def test_word2vec():
    wv = vectorizers.word2vec(wikitext.revision.datasources.words,
                              test_vectors, name='word vectors')
    vector = solve(wv, cache={ro.revision.text: 'a bv c d'})
    assert len(vector) == 4
    assert len(vector[0]) == 300
