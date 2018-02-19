"""
These Meta-Features genetate a :class:`revscoring.FeatureVector` based on some
:class:`revscoring.Datasource`.

.. autoclass revscoring.features.meta.vectorizers.vectorize
"""
import numpy as np
from .word2vec_helper import gensim_loader
from ..feature_vector import FeatureVector


class word_vectors(FeatureVector):
    """
    Constructs a :class:`revscoring.FeatureVector` that converts a
    dictionary into a list of values with a predictable order based on a set of
    keys.

    :Parameters:
        words_datasource : :class:`revscoring.Datasource`
            A datasource that returns a list of words.
        w2v_prefix : `string`
            prefix path where vectors are stores
        w2v : `string`
            name of word vector file to load
        returns : `func`
            A function that represents the type of value that will be
            contained in the vector.  When called without an argument, this
            function should return the default value (for missing) keys
            in the dict.
        dim : `int`
            The dimension of the vectors
        limit : `int`
            Max number of word vectors to load
        name : `str`
            A name for the `revscoring.FeatureVector`
    """

    def __init__(self, words_datasource, w2v_prefix="~/.word2vec/", w2v=None,
                 returns=np.float64, dim=300, limit=None, name=None):
        name = self._format_name(name, [words_datasource])
        self.prefix = w2v_prefix
        self.dim = dim
        self.limit = limit
        self.w2v = self.load_word2vec(w2v_prefix + w2v, limit)
        super().__init__(name, self.process, depends_on=[words_datasource],
                         returns=returns)

    def load_word2vec(self, path, limit):
        return gensim_loader(path, limit)

    def process(self, d):
        return np.mean([self.w2v[w] if w in self.w2v else np.zeros(self.dim)
                        for w in d], axis=0)
