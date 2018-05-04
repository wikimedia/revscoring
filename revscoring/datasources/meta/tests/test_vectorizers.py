import pickle
from unittest.mock import patch

import pytest
from revscoring.datasources import revision_oriented as ro
from revscoring.dependencies import solve
from revscoring.features import wikitext

from .. import vectorizers

test_vectors = {'a': [1] * 300,
                'b': [1] * 300,
                'c': [1] * 300}


def vectorize_words(words):
    return vectorizers.word2vec.vectorize_words(test_vectors, words)


def test_word2vec():
    wv = vectorizers.word2vec(wikitext.revision.datasources.words,
                              vectorize_words, name='word vectors')
    vector = solve(wv, cache={ro.revision.text: 'a bv c d'})
    assert len(vector) == 4
    assert len(vector[0]) == 300
    vector = solve(wv, cache={ro.revision.text: ''})
    assert len(vector) == 1
    assert len(vector[0]) == 300

    assert pickle.loads(pickle.dumps(wv)) == wv


@patch('gensim.models.keyedvectors')
def test_loadkv_path(kv):
    kv.KeyedVectors.load_word2vec_format.return_value = test_vectors
    vectorizers.KeyedVectors = kv.KeyedVectors
    vectors = vectorizers.word2vec.load_kv(path='foo')
    assert vectors is not None


@patch('gensim.models.keyedvectors')
def test_loadkv_filename_none(kv):
    kv.KeyedVectors.load_word2vec_format.side_effect = FileNotFoundError
    vectorizers.KeyedVectors = kv.KeyedVectors
    assert pytest.raises(FileNotFoundError,
                         vectorizers.word2vec.load_kv, filename='foo')
