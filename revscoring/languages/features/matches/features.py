from ....datasources.meta import dicts, filters
from ....dependencies import DependentSet
from ....features.meta import aggregators


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.datasources = revision_datasources

        self.matches = aggregators.len(self.datasources.matches)
        "`int` : A count of the number of matches found in the text"

        if hasattr(revision_datasources, 'parent'):
            self.parent = Revision(
                name + ".parent", revision_datasources.parent
            )
            """
            :class:`~revscoring.languages.features.regex_matches.Revision` :
            The parent revision
            """

        if hasattr(revision_datasources, 'diff'):
            self.diff = Diff(
                name + ".diff", revision_datasources.diff
            )
            """
            :class:`~revscoring.languages.features.regex_matches.Diff` : The
            difference made by this revision
            """


class Diff(DependentSet):

    def __init__(self, name, diff_datasources):
        super().__init__(name)
        self.datasources = diff_datasources

        self.matches_added = aggregators.len(self.datasources.matches_added)
        "`int` : The number of matches added in the edit"

        self.matches_removed = \
            aggregators.len(self.datasources.matches_removed)
        "`int` : The number of matches removed in the edit"

        match_delta_values = dicts.values(self.datasources.match_delta)
        self.match_delta_sum = aggregators.sum(
            match_delta_values,
            name=name + ".match_delta_sum",
            returns=int
        )
        "`int` : The sum of frequency delta for matched strings"
        self.match_delta_increase = aggregators.sum(
            filters.positive(match_delta_values),
            name=name + ".match_delta_increase",
            returns=int
        )
        "`int` : The sum of frequency delta increases for matched strings"
        self.match_delta_decrease = aggregators.sum(
            filters.negative(match_delta_values),
            name=name + ".match_delta_decrease",
            returns=int
        )
        "`int` : The sum of frequency delta decreases for matched strings"

        match_prop_delta_values = \
            dicts.values(self.datasources.match_prop_delta)
        self.match_prop_delta_sum = aggregators.sum(
            match_prop_delta_values,
            name=name + ".match_prop_delta_sum",
            returns=float
        )
        """
        `int` : The sum of proportional frequency delta for matched
        strings
        """
        self.match_prop_delta_increase = aggregators.sum(
            filters.positive(match_prop_delta_values),
            name=name + ".match_prop_delta_increase",
            returns=float
        )
        """
        `int` : The sum of proportional frequency delta increases for matched
        strings
        """
        self.match_prop_delta_decrease = aggregators.sum(
            filters.negative(match_prop_delta_values),
            name=name + ".match_prop_delta_decrease",
            returns=float
        )
        """
        `int` : The sum of proportional frequency delta decreases for matched
        strings
        """
