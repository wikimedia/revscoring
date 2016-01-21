from ....datasources.meta import dicts, filters
from ....dependencies import DependentSet
from ....features.meta import aggregators


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.datasources = revision_datasources

        self.stopwords = aggregators.len(self.datasources.stopwords)
        "`int` : A count of the number of stopwords in the content"
        self.non_stopwords = \
            aggregators.len(self.datasources.non_stopwords)
        "`int` : A count of the number of non-stopwords in the content"

        if hasattr(self.datasources, 'parent'):
            self.parent = Revision(name + ".parent", self.datasources.parent)
            """
            :class:`~revscoring.languages.features.stopwords.Revision` : The
            parent revision
            """

        if hasattr(self.datasources, 'diff'):
            self.diff = Diff(name + '.diff', self.datasources.diff)
            """
            :class:`~revscoring.languages.features.stopwords.Diff` : The
            parent revision
            """


class Diff(DependentSet):

    def __init__(self, name, diff_datasources):
        super().__init__(name)
        self.datasources = diff_datasources

        # Simple counts (based on wikitext.edit.diff)
        self.stopwords_added = \
            aggregators.len(self.datasources.stopwords_added)
        "`int` : A count of stopwords added"
        self.stopwords_removed = \
            aggregators.len(self.datasources.stopwords_removed)
        "`int` : A count of stopwords removed"
        self.non_stopwords_added = \
            aggregators.len(self.datasources.non_stopwords_added)
        "`int` : A count of non-stopwords added"
        self.non_stopwords_removed = \
            aggregators.len(self.datasources.non_stopwords_removed)
        "`int` : A count of non-stopwords removed"

        # Word frequency deltas
        stopword_delta_values = dicts.values(self.datasources.stopword_delta)
        self.stopword_delta_sum = aggregators.sum(
            stopword_delta_values,
            name=name + ".stopword_delta_sum",
            returns=int
        )
        "`int` : The sum of word frequency deltas for stopwords"
        self.stopword_delta_increase = aggregators.sum(
            filters.positive(stopword_delta_values),
            name=name + ".stopword_delta_increase",
            returns=int
        )
        "`int` : The sum of word frequency delta increases for stopwords"
        self.stopword_delta_decrease = aggregators.sum(
            filters.negative(stopword_delta_values),
            name=name + ".stopword_delta_decrease",
            returns=int
        )
        "`int` : The sum of word frequency delta decreases for stopwords"
        non_stopword_delta_values = \
            dicts.values(self.datasources.non_stopword_delta)
        self.non_stopword_delta_sum = aggregators.sum(
            non_stopword_delta_values,
            name=name + ".non_stopword_delta_sum",
            returns=int
        )
        "`int` : The sum of word frequency deltas for non-stopwords"
        self.non_stopword_delta_increase = aggregators.sum(
            filters.positive(non_stopword_delta_values),
            name=name + ".non_stopword_delta_increase",
            returns=int
        )
        "`int` : The sum of word frequency delta increases for non-stopwords"
        self.non_stopword_delta_decrease = aggregators.sum(
            filters.negative(non_stopword_delta_values),
            name=name + ".non_stopword_delta_decrease",
            returns=int
        )
        "`int` : The sum of word frequency delta decreases for non-stopwords"

        # Proportional word frequency deltas
        stopword_prop_delta_values = \
            dicts.values(self.datasources.stopword_prop_delta)
        self.stopword_prop_delta_sum = aggregators.sum(
            stopword_prop_delta_values,
            name=name + ".stopword_prop_delta_sum"
        )
        "`float` : The sum of proportional word frequency deltas for stopwords"
        self.stopword_prop_delta_increase = aggregators.sum(
            filters.positive(stopword_prop_delta_values),
            name=name + ".stopword_prop_delta_increase"
        )
        """
        `float` : The sum of proportional word frequency delta increases for
        stopwords
        """
        self.stopword_prop_delta_decrease = aggregators.sum(
            filters.negative(stopword_prop_delta_values),
            name=name + ".stopword_prop_delta_decrease"
        )
        """
        `float` : The sum of proportional word frequency delta decreases for
        stopwords
        """
        non_stopword_prop_delta_values = \
            dicts.values(self.datasources.non_stopword_prop_delta)
        self.non_stopword_prop_delta_sum = aggregators.sum(
            non_stopword_prop_delta_values,
            name=name + ".non_stopword_prop_delta_sum"
        )
        """
        `float` : The sum of proportional word frequency deltas for
        non-stopwords
        """
        self.non_stopword_prop_delta_increase = aggregators.sum(
            filters.positive(non_stopword_prop_delta_values),
            name=name + ".non_stopword_prop_delta_increase"
        )
        """
        `float` : The sum of proportional word frequency delta increases for
        non-stopwords
        """
        self.non_stopword_prop_delta_decrease = aggregators.sum(
            filters.negative(non_stopword_prop_delta_values),
            name=name + ".non_stopword_prop_delta_decrease"
        )
        """
        `float` : The sum of proportional word frequency delta decreases for
        non-stopwords
        """
