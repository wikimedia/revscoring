from ....datasources.meta import filters, frequencies, mappers
from ....features.wikitext import edit


class DictionaryRevision:

    def __init__(self, prefix, dictionary_check, words_datasource):
        self.dictionary_check = dictionary_check

        self.dict_words = filters.filter(
            self.is_dict_word, words_datasource,
            name=prefix + ".dict_words"
        )
        self.non_dict_words = filters.filter(
            self.is_not_dict_word, words_datasource,
            name=prefix + ".non_dict_words"
        )
        self.dict_word_frequency = frequencies.table(
            mappers.lower_case(self.dict_words),
            name=prefix + ".dict_word_frequency",
        )
        self.non_dict_word_frequency = frequencies.table(
            mappers.lower_case(self.non_dict_words),
            name=prefix + ".non_dict_word_frequency"
        )

    def is_dict_word(self, word):
        return self.dictionary_check(word)

    def is_not_dict_word(self, word):
        return not self.is_dict_word(word)


class DictionaryDiff:
    def __init__(self, prefix, dictionary_check,
                 revision_datasources, parent_datasources):
        self.dictionary_check = dictionary_check

        # Based on edit.diff
        self.dict_words_added = filters.filter(
            self.is_dict_word, edit.diff.datasources.words_added,
            name=prefix + ".dict_words_added"
        )
        self.dict_words_removed = filters.filter(
            self.is_dict_word, edit.diff.datasources.words_removed,
            name=prefix + ".dict_words_removed"
        )
        self.non_dict_words_added = filters.filter(
            self.is_not_dict_word, edit.diff.datasources.words_added,
            name=prefix + ".dict_words_added"
        )
        self.non_dict_words_removed = filters.filter(
            self.is_not_dict_word, edit.diff.datasources.words_removed,
            name=prefix + ".dict_words_removed"
        )

        # Frequencies
        self.dict_word_delta = frequencies.delta(
            parent_datasources.dict_word_frequency,
            revision_datasources.dict_word_frequency,
            name=prefix + ".dict_word_delta"
        )
        self.non_dict_word_delta = frequencies.delta(
            parent_datasources.non_dict_word_frequency,
            revision_datasources.non_dict_word_frequency,
            name=prefix + ".non_dict_word_delta"
        )

        self.dict_word_prop_delta = frequencies.prop_delta(
            parent_datasources.dict_word_frequency, self.dict_word_delta,
            name=prefix + ".dict_word_prop_delta"
        )
        self.non_dict_word_prop_delta = frequencies.prop_delta(
            parent_datasources.non_dict_word_frequency,
            self.non_dict_word_delta,
            name=prefix + ".non_dict_word_prop_delta"
        )

    def is_dict_word(self, word):
        return self.dictionary_check(word)

    def is_not_dict_word(self, word):
        return not self.is_dict_word(word)
