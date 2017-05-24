from ....datasources.meta import extractors, frequencies, mappers
from ....dependencies import DependentSet


class Revision(DependentSet):

    def __init__(self, name, regexes, wikitext_revision, exclusions, wrapping):
        super().__init__(name)

        self.matches = extractors.regex(
            regexes, wikitext_revision.text,
            name=name + ".matches",
            exclusions=exclusions,
            wrapping=wrapping
        )
        self.match_frequency = frequencies.table(
            mappers.lower_case(self.matches),
            name=name + ".match_frequency",
        )

        if hasattr(wikitext_revision, 'parent'):
            self.parent = Revision(name + ".parent", regexes,
                                   wikitext_revision.parent,
                                   exclusions=exclusions,
                                   wrapping=wrapping)

        if hasattr(wikitext_revision, 'diff'):
            self.diff = Diff(name + ".diff", regexes,
                             wikitext_revision.diff, self,
                             exclusions=exclusions,
                             wrapping=wrapping)


class Diff(DependentSet):

    def __init__(self, name, regexes, wikitext_diff,
                 revision, exclusions, wrapping):
        super().__init__(name)

        self.matches_added = extractors.regex(
            regexes, wikitext_diff.segments_added,
            name=name + ".matches_added",
            exclusions=exclusions,
            wrapping=wrapping
        )
        self.matches_removed = extractors.regex(
            regexes, wikitext_diff.segments_removed,
            name=name + ".matches_removed",
            exclusions=exclusions,
            wrapping=wrapping
        )

        self.match_delta = frequencies.delta(
            revision.parent.match_frequency,
            revision.match_frequency,
            name=name + ".match_delta"
        )
        self.match_prop_delta = frequencies.prop_delta(
            revision.parent.match_frequency,
            self.match_delta,
            name=name + ".match_prop_delta"
        )
