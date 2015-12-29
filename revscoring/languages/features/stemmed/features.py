from ....datasources.meta import dicts, filters, mappers
from ....dependencies import DependentSet
from ....features.meta import aggregators


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)

        self.datasources = revision_datasources

        self.unique_stems = aggregators.len(
            dicts.keys(self.datasources.stem_frequency),
            name=name + ".stems"
        )
        """
        `int` : A count of unique stemmed words.
        """

        self.stem_chars = aggregators.sum(
            mappers.map(len, self.datasources.stems),
            name=name + ".stems_length",
            returns=int
        )
        """
        `int` : A count of characters in stemmed words.
        """

        if hasattr(self.datasources, 'parent'):
            self.parent = Revision(name + ".parent", self.datasources.parent)
            """
            :class:`~revscoring.languages.features.stemmed.Revision` : The
            parent revision
            """

        if hasattr(self.datasources, 'diff'):
            self.diff = Diff(name + ".diff", self.datasources.diff)
            """
            :class:`~revscoring.languages.features.stemmed.Diff` : The
            diff between the parent and current revision.
            """


class Diff(DependentSet):

    def __init__(self, name, diff_datasources):
        super().__init__(name)
        self.datasources = diff_datasources

        self.stem_delta_sum = aggregators.sum(
            dicts.values(self.datasources.stem_delta),
            name=name + ".stem_delta_sum"
        )
        "`int` : The sum of frequency deltas for stemmed words"
        self.stem_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.stem_delta)),
            name=name + ".stem_delta_increase"
        )
        "`int` : The sum of frequency delta increases for stemmed words"
        self.stem_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.stem_delta)),
            name=name + ".stem_delta_decrease"
        )
        "`int` : The sum of frequency delta decreases for stemmed words"

        self.stem_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.stem_prop_delta),
            name=name + ".stem_prop_delta_sum"
        )
        "`int` : The sum of proportional frequency deltas for stemmed words"
        self.stem_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.stem_prop_delta)),
            name=name + ".stem_prop_delta_increase"
        )
        """
        `int` : The sum of proportional frequency delta increases for stemmed
        words
        """
        self.stem_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.stem_prop_delta)),
            name=name + ".stem_prop_delta_decrease"
        )
        """
        `int` : The sum of proportional frequency delta decreases for stemmed
        words
        """
