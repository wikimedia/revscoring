from ....datasources.meta import extractors, frequencies, mappers
from ....features.wikitext import edit


class RegexesRevision:

    def __init__(self, prefix, regexes, text_datasource):
        # Datasources
        self.matches = extractors.regex(
            regexes, text_datasource,
            name=prefix + ".matches",
        )
        self.match_frequency = frequencies.table(
            mappers.lower_case(self.matches),
            name=prefix + ".match_frequency",
        )


class RegexesDiff:

    def __init__(self, prefix, regexes, revision_datasources,
                 parent_revision_datasources):

        self.match_delta = frequencies.delta(
            parent_revision_datasources.match_frequency,
            revision_datasources.match_frequency,
            name=prefix + ".match_delta"
        )
        self.match_prop_delta = frequencies.prop_delta(
            parent_revision_datasources.match_frequency,
            self.match_delta,
            name=prefix + ".match_prop_delta"
        )

        self.matches_added = extractors.regex(
            regexes, edit.diff.datasources.segments_added,
            name=prefix + ".matches_added"
        )
        self.matches_removed = extractors.regex(
            regexes, edit.diff.datasources.segments_removed,
            name=prefix + ".matches_removed"
        )
