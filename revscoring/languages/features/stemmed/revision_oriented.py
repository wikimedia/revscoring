from . import datasources
from ....datasources.meta import dicts, filters, mappers
from ....features.meta import aggregators


class StemmedRevision:

    def __init__(self, prefix, stem_word, revision_words_datasource,
                 parent_words_datasource=None):

        self.datasources = datasources.StemmedRevision(
            prefix, stem_word,
            revision_words_datasource
        )

        self.unique_stems = aggregators.len(
            dicts.keys(self.datasources.stem_frequency),
            name=prefix + ".stems"
        )
        """
        A count of unique stemmed words.
        """

        self.stem_chars = aggregators.sum(
            mappers.map(len, self.datasources.stems),
            name=prefix + ".stems_length",
            returns=int
        )
        """
        A count of characters in stemmed words.
        """

        if parent_words_datasource is not None:
            self.parent = StemmedRevision(
                prefix + ".parent", stem_word,
                parent_words_datasource
            )


class StemmedDiff:

    def __init__(self, prefix, stem_word, revision_datasources,
                 parent_datasources):

        self.datasources = datasources.StemmedDiff(
            prefix, stem_word,
            revision_datasources, parent_datasources
        )

        self.stem_delta_sum = aggregators.sum(
            dicts.values(self.datasources.stem_delta),
            name=prefix + ".stem_delta_sum"
        )
        self.stem_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.stem_delta)),
            name=prefix + ".stem_delta_increase"
        )
        self.stem_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.stem_delta)),
            name=prefix + ".stem_delta_decrease"
        )

        self.stem_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.stem_prop_delta),
            name=prefix + ".stem_prop_delta_sum"
        )
        self.stem_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.stem_prop_delta)),
            name=prefix + ".stem_prop_delta_increase"
        )
        self.stem_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.stem_prop_delta)),
            name=prefix + ".stem_prop_delta_decrease"
        )
