from ...features import Feature


class Infonoise(Feature):

    def __init__(self, name, stopwords, stem_word, words_source):
        self.stopwords = set(stopwords)
        self.stem_word = stem_word
        super().__init__(name, self.process, returns=float,
                         depends_on=[words_source])

    def process(self, words):
        non_stopwords = (w for w in words if w.lower() not in self.stopwords)
        non_stopword_stems = (self.stem_word(w) for w in non_stopwords)

        length_of_stemmed = sum(len(w) for w in non_stopword_stems)

        if len(words) > 0:
            length_of_words = sum(len(w) for w in words)
        else:
            length_of_words = 0

        return length_of_stemmed / max(length_of_words, 1)
