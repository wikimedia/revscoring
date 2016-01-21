from ....datasources.meta import filters, frequencies, mappers
from ....dependencies import DependentSet


class Revision(DependentSet):

    def __init__(self, name, dictionary_check, wikitext_revision):
        super().__init__(name)
        self.dictionary_check = dictionary_check

        self.dict_words = filters.filter(
            dictionary_check, mappers.map(str, wikitext_revision.words),
            name=name + ".dict_words"
        )
        self.non_dict_words = filters.filter(
            dictionary_check, mappers.map(str, wikitext_revision.words),
            name=name + ".non_dict_words", inverse=True
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
