from gensim.models.keyedvectors import KeyedVectors


def gensim_loader(path, limit=None):
    return KeyedVectors.load_word2vec_format(path, binary=True, limit=limit)
