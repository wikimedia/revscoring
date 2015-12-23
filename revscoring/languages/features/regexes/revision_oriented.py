from . import datasources
from ....datasources.meta import dicts, filters
from ....features.meta import aggregators


class RegexesRevision:

    def __init__(self, prefix, regexes, revision_text_datasource,
                 parent_text_datasource=None):
        self.datasources = datasources.RegexesRevision(
            prefix, regexes,
            revision_text_datasource
        )

        self.matches = aggregators.len(self.datasources.matches)

        if parent_text_datasource is not None:
            self.parent = RegexesRevision(
                prefix + ".parent", regexes,
                parent_text_datasource
            )


class RegexesDiff:

    def __init__(self, prefix, regexes, revision_datasources,
                 parent_datasources):
        self.datasources = datasources.RegexesDiff(
            prefix, regexes,
            revision_datasources, parent_datasources
        )

        self.matches_added = aggregators.len(self.datasources.matches_added)
        self.matches_removed = \
            aggregators.len(self.datasources.matches_removed)

        match_delta_values = dicts.values(self.datasources.match_delta)
        self.match_delta_sum = aggregators.sum(
            match_delta_values,
            name=prefix + "match_delta_sum",
            returns=int
        )
        self.match_delta_increase = aggregators.sum(
            filters.positive(match_delta_values),
            name=prefix + "match_delta_increase",
            returns=int
        )
        self.match_delta_decrease = aggregators.sum(
            filters.negative(match_delta_values),
            name=prefix + "match_delta_decrease",
            returns=int
        )

        match_prop_delta_values = \
            dicts.values(self.datasources.match_prop_delta)
        self.match_prop_delta_sum = aggregators.sum(
            match_prop_delta_values,
            name=prefix + "match_prop_delta_sum",
            returns=float
        )
        self.match_prop_delta_increase = aggregators.sum(
            filters.positive(match_prop_delta_values),
            name=prefix + "match_prop_delta_increase",
            returns=float
        )
        self.match_prop_delta_decrease = aggregators.sum(
            filters.negative(match_prop_delta_values),
            name=prefix + "match_prop_delta_decrease",
            returns=float
        )
