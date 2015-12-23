from ....datasources.meta import filters, frequencies, mappers
from ....features.wikitext import edit


class StopwordsRevision:

    def __init__(self, prefix, stopwords_set, words_datasource):
        self.stopwords_set = stopwords_set

        self.stopwords = filters.filter(
            self.is_stopword, words_datasource,
            name=prefix + ".stopwords"
        )
        self.non_stopwords = filters.filter(
            self.is_not_stopword, words_datasource,
            name=prefix + ".non_stopwords"
        )
        self.stopword_frequency = frequencies.table(
            mappers.lower_case(self.stopwords),
            name=prefix + ".stopword_frequency",
        )
        self.non_stopword_frequency = frequencies.table(
            mappers.lower_case(self.non_stopwords),
            name=prefix + ".non_stopword_frequency"
        )

    def is_stopword(self, word):
        return word.lower() in self.stopwords_set

    def is_not_stopword(self, word):
        return word.lower() not in self.stopwords_set


class StopwordsDiff:
    def __init__(self, prefix, stopwords_set,
                 revision_datasources, parent_datasources):
        self.stopwords_set = stopwords_set

        # Based on edit.diff
        self.stopwords_added = filters.filter(
            self.is_stopword, edit.diff.datasources.words_added,
            name=prefix + ".diff.stopwords_added"
        )
        self.stopwords_removed = filters.filter(
            self.is_stopword, edit.diff.datasources.words_removed,
            name=prefix + ".diff.stopwords_removed"
        )
        self.non_stopwords_added = filters.filter(
            self.is_not_stopword, edit.diff.datasources.words_added,
            name=prefix + ".diff.stopwords_added"
        )
        self.non_stopwords_removed = filters.filter(
            self.is_not_stopword, edit.diff.datasources.words_removed,
            name=prefix + ".diff.stopwords_removed"
        )

        # Frequencies
        self.stopword_delta = frequencies.delta(
            parent_datasources.stopword_frequency,
            revision_datasources.stopword_frequency,
            name=prefix + ".diff.stopword_delta"
        )
        self.non_stopword_delta = frequencies.delta(
            parent_datasources.non_stopword_frequency,
            revision_datasources.non_stopword_frequency,
            name=prefix + ".diff.non_stopword_delta"
        )

        self.stopword_prop_delta = frequencies.prop_delta(
            parent_datasources.stopword_frequency,
            self.stopword_delta,
            name=prefix + ".diff.stopword_prop_delta"
        )
        self.non_stopword_prop_delta = frequencies.prop_delta(
            parent_datasources.non_stopword_frequency,
            self.non_stopword_delta,
            name=prefix + ".diff.non_stopword_prop_delta"
        )

    def is_stopword(self, word):
        return word.lower() in self.stopwords_set

    def is_not_stopword(self, word):
        return word.lower() not in self.stopwords_set
