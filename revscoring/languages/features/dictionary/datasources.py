from ....datasources import Datasource
from ....datasources.meta import filters, frequencies, mappers
from ....dependencies import DependentSet


class Revision(DependentSet):

    def __init__(self, name, dictionary_check, wikitext_revision):
        super().__init__(name)
        self.dictionary_check = dictionary_check

        self.dict_split = dict_splitter(
            name + '.dict_split', dictionary_check, wikitext_revision.words
        )
        self.dict_words = Datasource(
            name + '.dict_words', _process_dict_words,
            depends_on=[self.dict_split]
        )
        self.non_dict_words = Datasource(
            name + '.non_dict_words', _process_non_dict_words,
            depends_on=[self.dict_split]
        )
        self.dict_word_frequency = frequencies.table(
            mappers.lower_case(self.dict_words),
            name=name + ".dict_word_frequency",
        )
        self.non_dict_word_frequency = frequencies.table(
            mappers.lower_case(self.non_dict_words),
            name=name + ".non_dict_word_frequency"
        )

        if hasattr(wikitext_revision, 'parent'):
            self.parent = Revision(name + ".parent", dictionary_check,
                                   wikitext_revision.parent)

        if hasattr(wikitext_revision, 'diff'):
            self.diff = Diff(name + ".diff", dictionary_check,
                             wikitext_revision.diff, self)


def _process_dict_words(dict_split):
    return dict_split[0]


def _process_non_dict_words(dict_split):
    return dict_split[1]


class dict_splitter(Datasource):

    def __init__(self, name, dictionary_check, words_datasource):
        name = self._format_name(name, [dictionary_check, words_datasource])
        self.dictionary_check = dictionary_check
        super().__init__(name, self.process, depends_on=[words_datasource])

    def process(self, words):
        dict_words = []
        non_dict_words = []
        for word in words:
            if self.dictionary_check(str(word)):
                dict_words.append(word)
            else:
                non_dict_words.append(word)

        return dict_words, non_dict_words


class Diff(DependentSet):
    def __init__(self, name, dictionary_check, wikitext_diff, revision):
        super().__init__(name)
        self.dictionary_check = dictionary_check

        # Based on edit.diff
        self.dict_words_added = filters.filter(
            dictionary_check, mappers.map(str, wikitext_diff.words_added),
            name=name + ".dict_words_added"
        )
        self.dict_words_removed = filters.filter(
            dictionary_check, mappers.map(str, wikitext_diff.words_removed),
            name=name + ".dict_words_removed"
        )
        self.non_dict_words_added = filters.filter(
            dictionary_check, mappers.map(str, wikitext_diff.words_added),
            name=name + ".non_dict_words_added", inverse=True
        )
        self.non_dict_words_removed = filters.filter(
            dictionary_check, mappers.map(str, wikitext_diff.words_removed),
            name=name + ".non_dict_words_removed", inverse=True
        )

        # Frequencies
        self.dict_word_delta = frequencies.delta(
            revision.parent.dict_word_frequency,
            revision.dict_word_frequency,
            name=name + ".dict_word_delta"
        )
        self.non_dict_word_delta = frequencies.delta(
            revision.parent.non_dict_word_frequency,
            revision.non_dict_word_frequency,
            name=name + ".non_dict_word_delta"
        )

        self.dict_word_prop_delta = frequencies.prop_delta(
            revision.parent.dict_word_frequency, self.dict_word_delta,
            name=name + ".dict_word_prop_delta"
        )
        self.non_dict_word_prop_delta = frequencies.prop_delta(
            revision.parent.non_dict_word_frequency,
            self.non_dict_word_delta,
            name=name + ".non_dict_word_prop_delta"
        )
