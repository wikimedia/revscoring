from . import datasources
from ....datasources.meta import dicts, filters
from ....features.meta import aggregators


class DictionaryRevision:

    def __init__(self, prefix, dictionary_check,
                 words_datasource,
                 parent_words_datasource=None):

        self.datasources = datasources.DictionaryRevision(
            prefix, dictionary_check, words_datasource
        )

        self.dict_words = aggregators.len(self.datasources.dict_words)
        self.non_dict_words = \
            aggregators.len(self.datasources.non_dict_words)

        if parent_words_datasource is not None:
            self.parent = DictionaryRevision(
                prefix + ".parent", dictionary_check,
                parent_words_datasource
            )


class DictionaryDiff:

    def __init__(self, prefix, dictionary_check, revision_datasources,
                 parent_datasources):

        self.datasources = datasources.DictionaryDiff(
            prefix, dictionary_check, revision_datasources,
            parent_datasources
        )

        # Simple counts (based on wikitext.edit.diff)
        self.dict_words_added = \
            aggregators.len(self.datasources.dict_words_added)
        self.dict_words_removed = \
            aggregators.len(self.datasources.dict_words_removed)
        self.non_dict_words_added = \
            aggregators.len(self.datasources.non_dict_words_added)
        self.non_dict_words_removed = \
            aggregators.len(self.datasources.non_dict_words_removed)

        # Word frequency deltas
        dict_word_delta_values = dicts.values(self.datasources.dict_word_delta)
        self.dict_word_delta_sum = aggregators.sum(
            dict_word_delta_values,
            name=prefix + ".dict_word_delta_sum",
            returns=int
        )
        self.dict_word_delta_increase = aggregators.sum(
            filters.positive(dict_word_delta_values),
            name=prefix + ".dict_word_delta_increase",
            returns=int
        )
        self.dict_word_delta_decrease = aggregators.sum(
            filters.negative(dict_word_delta_values),
            name=prefix + ".dict_word_delta_decrease",
            returns=int
        )
        non_dict_word_delta_values = \
            dicts.values(self.datasources.non_dict_word_delta)
        self.non_dict_word_delta_sum = aggregators.sum(
            non_dict_word_delta_values,
            name=prefix + ".dict_word_delta_sum",
            returns=int
        )
        self.non_dict_word_delta_increase = aggregators.sum(
            filters.positive(non_dict_word_delta_values),
            name=prefix + ".non_dict_word_delta_increase",
            returns=int
        )
        self.non_dict_word_delta_decrease = aggregators.sum(
            filters.negative(non_dict_word_delta_values),
            name=prefix + ".non_dict_word_delta_decrease",
            returns=int
        )

        # Proportional word frequency deltas
        dict_word_prop_delta_values = \
            dicts.values(self.datasources.dict_word_prop_delta)
        self.dict_word_prop_delta_sum = aggregators.sum(
            dict_word_prop_delta_values,
            name=prefix + ".dict_word_prop_delta_sum"
        )
        self.dict_word_prop_delta_increase = aggregators.sum(
            filters.positive(dict_word_prop_delta_values),
            name=prefix + ".dict_word_prop_delta_increase"
        )
        self.dict_word_prop_delta_decrease = aggregators.sum(
            filters.negative(dict_word_prop_delta_values),
            name=prefix + ".dict_word_prop_delta_decrease"
        )

        non_dict_word_prop_delta_values = \
            dicts.values(self.datasources.non_dict_word_prop_delta)
        self.non_dict_word_prop_delta_sum = aggregators.sum(
            non_dict_word_prop_delta_values,
            name=prefix + ".non_dict_word_prop_delta_sum"
        )
        self.non_dict_word_prop_delta_increase = aggregators.sum(
            filters.positive(non_dict_word_prop_delta_values),
            name=prefix + ".non_dict_word_prop_delta_increase"
        )
        self.non_dict_word_prop_delta_decrease = aggregators.sum(
            filters.negative(non_dict_word_prop_delta_values),
            name=prefix + ".non_dict_word_prop_delta_decrease"
        )
