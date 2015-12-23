from ....datasources.meta import frequencies, mappers
from ....features.wikitext import edit


class StemmedRevision:
    def __init__(self, prefix, stem_word, words_datasource):

        self.stems = mappers.map(
            stem_word, words_datasource,
            name=prefix + ".stems"
        )

        self.stem_frequency = frequencies.table(
            self.stems,
            name=prefix + ".stem_frequency"
        )


class StemmedDiff:
    def __init__(self, prefix, stem_word, revision_datasources,
                 parent_datasources):

        self.stems_added = mappers.map(
            stem_word, edit.diff.datasources.words_added,
            name=prefix + ".stems_added"
        )
        self.stems_removed = mappers.map(
            stem_word, edit.diff.datasources.words_removed,
            name=prefix + ".stems_removed"
        )

        self.stem_delta = frequencies.delta(
            parent_datasources.stem_frequency,
            revision_datasources.stem_frequency,
            name=prefix + ".stem_delta"
        )
        self.stem_prop_delta = frequencies.prop_delta(
            parent_datasources.stem_frequency, self.stem_delta,
            name=prefix + ".stem_prop_delta"
        )
