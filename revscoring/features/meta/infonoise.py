from ...features import Feature


class infonoise(MetaFeature):

    def __init__(self, name, words_datasource,
                 stemmed_non_stopwords_datasource):
        super().__init__(name=name, returns=float,
                         depends_on=[words_datasource,
                                     stemmed_non_stopwords_datasource])

    def process(self, words, stemmed_non_stopwords):
        length_of_stemmed = sum(len(w) for w in stemmed_non_stopwords)
        length_of_words = sum(len(w) for w in words)

        return length_of_stemmed / max(length_of_words, 1)
