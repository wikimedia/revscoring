from . import datasources
from ....datasources.meta import dicts, filters
from ....dependencies import DependentSet
from ....features.meta import aggregators


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.datasources = revision_datasources

        self.stopwords = aggregators.len(self.datasources.stopwords)
        self.non_stopwords = \
            aggregators.len(self.datasources.non_stopwords)

        if hasattr(self.datasources, 'parent'):
            self.parent = Revision(name + ".parent", self.datasources.parent)

        if hasattr(self.datasources, 'diff'):
            self.diff = Diff(name + '.diff', self.datasources.diff)


class Diff(DependentSet):

    def __init__(self, name, diff_datasources):
        super().__init__(name)
        self.datasources = diff_datasources

        # Simple counts (based on wikitext.edit.diff)
        self.stopwords_added = \
            aggregators.len(self.datasources.stopwords_added)
        self.stopwords_removed = \
            aggregators.len(self.datasources.stopwords_removed)
        self.non_stopwords_added = \
            aggregators.len(self.datasources.non_stopwords_added)
        self.non_stopwords_removed = \
            aggregators.len(self.datasources.non_stopwords_removed)

        # Word frequency deltas
        stopword_delta_values = dicts.values(self.datasources.stopword_delta)
        self.stopword_delta_sum = aggregators.sum(
            stopword_delta_values,
            name=name + ".stopword_delta_sum",
            returns=int
        )
        self.stopword_delta_increase = aggregators.sum(
            filters.positive(stopword_delta_values),
            name=name + ".stopword_delta_increase",
            returns=int
        )
        self.stopword_delta_decrease = aggregators.sum(
            filters.negative(stopword_delta_values),
            name=name + ".stopword_delta_decrease",
            returns=int
        )
        non_stopword_delta_values = \
            dicts.values(self.datasources.non_stopword_delta)
        self.non_stopword_delta_sum = aggregators.sum(
            non_stopword_delta_values,
            name=name + ".non_stopword_delta_sum",
            returns=int
        )
        self.non_stopword_delta_increase = aggregators.sum(
            filters.positive(non_stopword_delta_values),
            name=name + ".non_stopword_delta_increase",
            returns=int
        )
        self.non_stopword_delta_decrease = aggregators.sum(
            filters.negative(non_stopword_delta_values),
            name=name + ".non_stopword_delta_decrease",
            returns=int
        )

        # Proportional word frequency deltas
        stopword_prop_delta_values = \
            dicts.values(self.datasources.stopword_prop_delta)
        self.stopword_prop_delta_sum = aggregators.sum(
            stopword_prop_delta_values,
            name=name + ".stopword_prop_delta_sum"
        )
        self.stopword_prop_delta_increase = aggregators.sum(
            filters.positive(stopword_prop_delta_values),
            name=name + ".stopword_prop_delta_increase"
        )
        self.stopword_prop_delta_decrease = aggregators.sum(
            filters.negative(stopword_prop_delta_values),
            name=name + ".stopword_prop_delta_decrease"
        )
        non_stopword_prop_delta_values = \
            dicts.values(self.datasources.non_stopword_prop_delta)
        self.non_stopword_prop_delta_sum = aggregators.sum(
            non_stopword_prop_delta_values,
            name=name + ".non_stopword_prop_delta_sum"
        )
        self.non_stopword_prop_delta_increase = aggregators.sum(
            filters.positive(non_stopword_prop_delta_values),
            name=name + ".non_stopword_prop_delta_increase"
        )
        self.non_stopword_prop_delta_decrease = aggregators.sum(
            filters.negative(non_stopword_prop_delta_values),
            name=name + ".non_stopword_prop_delta_decrease"
        )
