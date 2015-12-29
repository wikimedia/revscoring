from ....datasources.meta import dicts, filters
from ....dependencies import DependentSet
from ....features.meta import aggregators


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.datasources = revision_datasources

        self.dict_words = aggregators.len(self.datasources.dict_words)
        "`int` : A count of the number of dictionary words in the revision"
        self.non_dict_words = \
            aggregators.len(self.datasources.non_dict_words)
        "`int` : A count of the number of non-dictionary words in the revision"

        if hasattr(self.datasources, 'parent'):
            self.parent = Revision(name + ".parent", self.datasources.parent)
            """
            :class:`~revscoring.languages.features.dictionary.Revision` : The
            parent revision
            """

        if hasattr(self.datasources, 'diff'):
            self.diff = Diff(name + ".diff", self.datasources.diff)
            """
            :class:`~revscoring.languages.features.dictionary.Diff` : The
            diff between the parent and current revision.
            """


class Diff(DependentSet):

    def __init__(self, name, diff_datasources):
        super().__init__(name)
        self.datasources = diff_datasources

        # Simple counts (based on wikitext.edit.diff)
        self.dict_words_added = \
            aggregators.len(self.datasources.dict_words_added)
        "`int` : A count of the number of dictionary words added"
        self.dict_words_removed = \
            aggregators.len(self.datasources.dict_words_removed)
        "`int` : A count of the number of dictionary words removed"
        self.non_dict_words_added = \
            aggregators.len(self.datasources.non_dict_words_added)
        "`int` : A count of the number of non-dictionary words added"
        self.non_dict_words_removed = \
            aggregators.len(self.datasources.non_dict_words_removed)
        "`int` : A count of the number of non-dictionary words removed"

        # Word frequency deltas
        dict_word_delta_values = dicts.values(self.datasources.dict_word_delta)
        self.dict_word_delta_sum = aggregators.sum(
            dict_word_delta_values,
            name=name + ".dict_word_delta_sum",
            returns=int
        )
        "`int` : The sum of word frequency deltas for dictionary words"
        self.dict_word_delta_increase = aggregators.sum(
            filters.positive(dict_word_delta_values),
            name=name + ".dict_word_delta_increase",
            returns=int
        )
        """
        `int` : The sum of word frequency delta increases for dictionary words
        """
        self.dict_word_delta_decrease = aggregators.sum(
            filters.negative(dict_word_delta_values),
            name=name + ".dict_word_delta_decrease",
            returns=int
        )
        """
        `int` : The sum of word frequency delta decreases for dictionary
        words
        """
        non_dict_word_delta_values = \
            dicts.values(self.datasources.non_dict_word_delta)
        self.non_dict_word_delta_sum = aggregators.sum(
            non_dict_word_delta_values,
            name=name + ".non_dict_word_delta_sum",
            returns=int
        )
        "`int` : The sum of word frequency deltas for non-dictionary words"
        self.non_dict_word_delta_increase = aggregators.sum(
            filters.positive(non_dict_word_delta_values),
            name=name + ".non_dict_word_delta_increase",
            returns=int
        )
        """
        `int` : The sum of word frequency delta increases for non-dictionary
        words
        """
        self.non_dict_word_delta_decrease = aggregators.sum(
            filters.negative(non_dict_word_delta_values),
            name=name + ".non_dict_word_delta_decrease",
            returns=int
        )
        """
        `int` : The sum of word frequency delta decreases for non-dictionary
        words
        """

        # Proportional word frequency deltas
        dict_word_prop_delta_values = \
            dicts.values(self.datasources.dict_word_prop_delta)
        self.dict_word_prop_delta_sum = aggregators.sum(
            dict_word_prop_delta_values,
            name=name + ".dict_word_prop_delta_sum"
        )
        """
        `float` : The sum of word frequency proportional delta for
        dictionary words
        """
        self.dict_word_prop_delta_increase = aggregators.sum(
            filters.positive(dict_word_prop_delta_values),
            name=name + ".dict_word_prop_delta_increase"
        )
        """
        `float` : The sum of word frequency proportional delta increases for
        dictionary words
        """
        self.dict_word_prop_delta_decrease = aggregators.sum(
            filters.negative(dict_word_prop_delta_values),
            name=name + ".dict_word_prop_delta_decrease"
        )
        """
        `float` : The sum of word frequency proportional delta decreases for
        dictionary words
        """

        non_dict_word_prop_delta_values = \
            dicts.values(self.datasources.non_dict_word_prop_delta)
        self.non_dict_word_prop_delta_sum = aggregators.sum(
            non_dict_word_prop_delta_values,
            name=name + ".non_dict_word_prop_delta_sum"
        )
        """
        `float` : The sum of word frequency proportional delta for
        non-dictionary words
        """
        self.non_dict_word_prop_delta_increase = aggregators.sum(
            filters.positive(non_dict_word_prop_delta_values),
            name=name + ".non_dict_word_prop_delta_increase"
        )
        """
        `float` : The sum of word frequency proportional delta increase for
        non-dictionary words
        """
        self.non_dict_word_prop_delta_decrease = aggregators.sum(
            filters.negative(non_dict_word_prop_delta_values),
            name=name + ".non_dict_word_prop_delta_decrease"
        )
        """
        `float` : The sum of word frequency proportional delta decrease for
        non-dictionary words
        """
