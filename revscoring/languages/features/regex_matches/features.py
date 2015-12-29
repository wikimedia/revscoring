from ....datasources.meta import dicts, filters
from ....dependencies import DependentSet
from ....features.meta import aggregators


class Revision(DependentSet):

    def __init__(self, name, regexes, revision_datasources):
        super().__init__(name)
        self.datasources = revision_datasources

        self.matches = aggregators.len(self.datasources.matches)

        if hasattr(revision_datasources, 'parent'):
            self.parent = Revision(
                name + ".parent", regexes, revision_datasources.parent
            )

        if hasattr(revision_datasources, 'diff'):
            self.diff = Diff(
                name + ".diff", regexes, revision_datasources.diff
            )


class Diff(DependentSet):

    def __init__(self, name, regexes, diff_datasources):
        super().__init__(name)
        self.datasources = diff_datasources

        self.matches_added = aggregators.len(self.datasources.matches_added)
        self.matches_removed = \
            aggregators.len(self.datasources.matches_removed)

        match_delta_values = dicts.values(self.datasources.match_delta)
        self.match_delta_sum = aggregators.sum(
            match_delta_values,
            name=name + "match_delta_sum",
            returns=int
        )
        self.match_delta_increase = aggregators.sum(
            filters.positive(match_delta_values),
            name=name + "match_delta_increase",
            returns=int
        )
        self.match_delta_decrease = aggregators.sum(
            filters.negative(match_delta_values),
            name=name + "match_delta_decrease",
            returns=int
        )

        match_prop_delta_values = \
            dicts.values(self.datasources.match_prop_delta)
        self.match_prop_delta_sum = aggregators.sum(
            match_prop_delta_values,
            name=name + "match_prop_delta_sum",
            returns=float
        )
        self.match_prop_delta_increase = aggregators.sum(
            filters.positive(match_prop_delta_values),
            name=name + "match_prop_delta_increase",
            returns=float
        )
        self.match_prop_delta_decrease = aggregators.sum(
            filters.negative(match_prop_delta_values),
            name=name + "match_prop_delta_decrease",
            returns=float
        )
