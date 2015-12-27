from ....datasources.meta import dicts, filters
from ...meta import aggregators


class Revision:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tokens = aggregators.len(self.datasources.tokens)
        self.numbers = aggregators.len(self.datasources.numbers)
        self.whitespaces = aggregators.len(self.datasources.whitespaces)
        self.markups = aggregators.len(self.datasources.markups)
        self.cjks = aggregators.len(self.datasources.cjks)
        self.entities = aggregators.len(self.datasources.entities)
        self.urls = aggregators.len(self.datasources.urls)
        self.words = aggregators.len(self.datasources.words)
        self.uppercase_words = \
            aggregators.len(self.datasources.uppercase_words)
        self.punctuations = aggregators.len(self.datasources.punctuations)
        self.breaks = aggregators.len(self.datasources.breaks)


class Diff:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.token_delta_sum = aggregators.sum(
            dicts.values(self.datasources.token_delta),
            name=self._name + ".token_delta_sum"
        )
        """
        The sum of delta changes in the token frequency table
        """

        self.token_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.token_delta)),
            name=self._name + ".token_delta_increase"
        )
        """
        The sum of delta increases in the token frequency table
        """

        self.token_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.token_delta)),
            name=self._name + ".token_delta_decrease"
        )
        """
        The sum of delta decreases in the token frequency table
        """

        self.token_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.token_prop_delta),
            name=self._name + ".token_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the token frequency table
        """

        self.token_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.token_prop_delta)),
            name=self._name + ".token_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the token frequency table
        """

        self.token_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.token_prop_delta)),
            name=self._name + ".token_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the token frequency table
        """

        # number
        self.number_delta_sum = aggregators.sum(
            dicts.values(self.datasources.number_delta),
            name=self._name + ".number_delta_sum"
        )
        """
        The sum of delta changes in the number frequency table
        """

        self.number_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.number_delta)),
            name=self._name + ".number_delta_increase"
        )
        """
        The sum of delta increases in the number frequency table
        """

        self.number_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.number_delta)),
            name=self._name + ".number_delta_decrease"
        )
        """
        The sum of delta decreases in the number frequency table
        """

        self.number_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.number_prop_delta),
            name=self._name + ".number_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the number frequency table
        """

        self.number_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.number_prop_delta)),
            name=self._name + ".number_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the number frequency table
        """

        self.number_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.number_prop_delta)),
            name=self._name + ".number_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the number frequency table
        """

        # whitespace
        self.whitespace_delta_sum = aggregators.sum(
            dicts.values(self.datasources.whitespace_delta),
            name=self._name + ".whitespace_delta_sum"
        )
        """
        The sum of delta changes in the whitespace frequency table
        """

        self.whitespace_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.whitespace_delta)),
            name=self._name + ".whitespace_delta_increase"
        )
        """
        The sum of delta increases in the whitespace frequency table
        """

        self.whitespace_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.whitespace_delta)),
            name=self._name + ".whitespace_delta_decrease"
        )
        """
        The sum of delta decreases in the whitespace frequency table
        """

        self.whitespace_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.whitespace_prop_delta),
            name=self._name + ".whitespace_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the whitespace frequency table
        """

        self.whitespace_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(
                self.datasources.whitespace_prop_delta)),
            name=self._name + ".whitespace_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the whitespace frequency
        table
        """

        self.whitespace_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(
                self.datasources.whitespace_prop_delta)),
            name=self._name + ".whitespace_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the whitespace frequency
        table
        """

        # markup
        self.markup_delta_sum = aggregators.sum(
            dicts.values(self.datasources.markup_delta),
            name=self._name + ".markup_delta_sum"
        )
        """
        The sum of delta changes in the markup frequency table
        """

        self.markup_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.markup_delta)),
            name=self._name + ".markup_delta_increase"
        )
        """
        The sum of delta increases in the markup frequency table
        """

        self.markup_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.markup_delta)),
            name=self._name + ".markup_delta_decrease"
        )
        """
        The sum of delta decreases in the markup frequency table
        """

        self.markup_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.markup_prop_delta),
            name=self._name + ".markup_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the markup frequency table
        """

        self.markup_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.markup_prop_delta)),
            name=self._name + ".markup_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the markup frequency table
        """

        self.markup_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.markup_prop_delta)),
            name=self._name + ".markup_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the markup frequency table
        """

        # cjk
        self.cjk_delta_sum = aggregators.sum(
            dicts.values(self.datasources.cjk_delta),
            name=self._name + ".cjk_delta_sum"
        )
        """
        The sum of delta changes in the cjk frequency table
        """

        self.cjk_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.cjk_delta)),
            name=self._name + ".cjk_delta_increase"
        )
        """
        The sum of delta increases in the cjk frequency table
        """

        self.cjk_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.cjk_delta)),
            name=self._name + ".cjk_delta_decrease"
        )
        """
        The sum of delta decreases in the cjk frequency table
        """

        self.cjk_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.cjk_prop_delta),
            name=self._name + ".cjk_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the cjk frequency table
        """

        self.cjk_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.cjk_prop_delta)),
            name=self._name + ".cjk_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the cjk frequency table
        """

        self.cjk_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.cjk_prop_delta)),
            name=self._name + ".cjk_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the cjk frequency table
        """

        # entity
        self.entity_delta_sum = aggregators.sum(
            dicts.values(self.datasources.entity_delta),
            name=self._name + ".entity_delta_sum"
        )
        """
        The sum of delta changes in the entity frequency table
        """

        self.entity_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.entity_delta)),
            name=self._name + ".entity_delta_increase"
        )
        """
        The sum of delta increases in the entity frequency table
        """

        self.entity_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.entity_delta)),
            name=self._name + ".entity_delta_decrease"
        )
        """
        The sum of delta decreases in the entity frequency table
        """

        self.entity_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.entity_prop_delta),
            name=self._name + ".entity_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the entity frequency table
        """

        self.entity_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.entity_prop_delta)),
            name=self._name + ".entity_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the entity frequency table
        """

        self.entity_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.entity_prop_delta)),
            name=self._name + ".entity_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the entity frequency table
        """

        # url
        self.url_delta_sum = aggregators.sum(
            dicts.values(self.datasources.url_delta),
            name=self._name + ".url_delta_sum"
        )
        """
        The sum of delta changes in the url frequency table
        """

        self.url_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.url_delta)),
            name=self._name + ".url_delta_increase"
        )
        """
        The sum of delta increases in the url frequency table
        """

        self.url_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.url_delta)),
            name=self._name + ".url_delta_decrease"
        )
        """
        The sum of delta decreases in the url frequency table
        """

        self.url_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.url_prop_delta),
            name=self._name + ".url_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the url frequency table
        """

        self.url_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.url_prop_delta)),
            name=self._name + ".url_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the url frequency table
        """

        self.url_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.url_prop_delta)),
            name=self._name + ".url_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the url frequency table
        """

        # word
        self.word_delta_sum = aggregators.sum(
            dicts.values(self.datasources.word_delta),
            name=self._name + ".word_delta_sum"
        )
        """
        The sum of delta changes in the word frequency table
        """

        self.word_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.word_delta)),
            name=self._name + ".word_delta_increase"
        )
        """
        The sum of delta increases in the word frequency table
        """

        self.word_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.word_delta)),
            name=self._name + ".word_delta_decrease"
        )
        """
        The sum of delta decreases in the word frequency table
        """

        self.word_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.word_prop_delta),
            name=self._name + ".word_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the word frequency table
        """

        self.word_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.word_prop_delta)),
            name=self._name + ".word_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the word frequency table
        """

        self.word_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.word_prop_delta)),
            name=self._name + ".word_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the word frequency table
        """

        # punctuation
        self.punctuation_delta_sum = aggregators.sum(
            dicts.values(self.datasources.punctuation_delta),
            name=self._name + ".punctuation_delta_sum"
        )
        """
        The sum of delta changes in the punctuation frequency table
        """

        self.punctuation_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.punctuation_delta)),
            name=self._name + ".punctuation_delta_increase"
        )
        """
        The sum of delta increases in the punctuation frequency table
        """

        self.punctuation_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.punctuation_delta)),
            name=self._name + ".punctuation_delta_decrease"
        )
        """
        The sum of delta decreases in the punctuation frequency table
        """

        self.punctuation_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.punctuation_prop_delta),
            name=self._name + ".punctuation_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the punctuation frequency
        table
        """

        self.punctuation_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(
                self.datasources.punctuation_prop_delta)),
            name=self._name + ".punctuation_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the punctuation frequency
        table
        """

        self.punctuation_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(
                self.datasources.punctuation_prop_delta)),
            name=self._name + ".punctuation_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the punctuation frequency
        table
        """

        # break
        self.break_delta_sum = aggregators.sum(
            dicts.values(self.datasources.break_delta),
            name=self._name + ".break_delta_sum"
        )
        """
        The sum of delta changes in the break frequency table
        """

        self.break_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.break_delta)),
            name=self._name + ".break_delta_increase"
        )
        """
        The sum of delta increases in the break frequency table
        """

        vbreak_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.break_delta)),
            name=self._name + ".break_delta_decrease"
        )
        """
        The sum of delta decreases in the break frequency table
        """

        self.break_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.break_prop_delta),
            name=self._name + ".break_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the break frequency table
        """

        self.break_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.break_prop_delta)),
            name=self._name + ".break_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the break frequency table
        """

        self.break_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.break_prop_delta)),
            name=self._name + ".break_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the break frequency table
        """
