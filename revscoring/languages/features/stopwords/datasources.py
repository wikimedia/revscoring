from ....datasources.meta import filters, frequencies, mappers
from ....dependencies import DependentSet


class Revision(DependentSet):

    def __init__(self, name, is_stopword, wikitext_revision):
        super().__init__(name)

        self.stopwords = filters.filter(
            is_stopword, wikitext_revision.words,
            name=name + ".stopwords"
        )
        self.non_stopwords = filters.filter(
            is_stopword, wikitext_revision.words,
            name=name + ".non_stopwords", inverse=True
        )
        self.stopword_frequency = frequencies.table(
            mappers.lower_case(self.stopwords),
            name=name + ".stopword_frequency",
        )
        self.non_stopword_frequency = frequencies.table(
            mappers.lower_case(self.non_stopwords),
            name=name + ".non_stopword_frequency"
        )

        if hasattr(wikitext_revision, 'parent'):
            self.parent = Revision(name + 'parent', is_stopword,
                                   wikitext_revision.parent)

        if hasattr(wikitext_revision, 'diff'):
            self.diff = Diff(name, is_stopword, wikitext_revision.diff, self)


class Diff(DependentSet):
    def __init__(self, name, is_stopword, wikitext_diff, revision):
        super().__init__(name)
        self.is_stopword = is_stopword

        # Based on edit.diff
        self.stopwords_added = filters.filter(
            is_stopword, wikitext_diff.words_added,
            name=name + ".diff.stopwords_added"
        )
        self.stopwords_removed = filters.filter(
            is_stopword, wikitext_diff.words_removed,
            name=name + ".diff.stopwords_removed"
        )
        self.non_stopwords_added = filters.filter(
            is_stopword, wikitext_diff.words_added,
            name=name + ".diff.non_stopwords_added", inverse=True
        )
        self.non_stopwords_removed = filters.filter(
            is_stopword, wikitext_diff.words_removed,
            name=name + ".diff.non_stopwords_removed", inverse=True
        )

        # Frequencies
        self.stopword_delta = frequencies.delta(
            revision.parent.stopword_frequency,
            revision.stopword_frequency,
            name=name + ".diff.stopword_delta"
        )
        self.non_stopword_delta = frequencies.delta(
            revision.parent.non_stopword_frequency,
            revision.non_stopword_frequency,
            name=name + ".diff.non_stopword_delta"
        )

        self.stopword_prop_delta = frequencies.prop_delta(
            revision.parent.stopword_frequency,
            self.stopword_delta,
            name=name + ".diff.stopword_prop_delta"
        )
        self.non_stopword_prop_delta = frequencies.prop_delta(
            revision.parent.non_stopword_frequency,
            self.non_stopword_delta,
            name=name + ".diff.non_stopword_prop_delta"
        )
