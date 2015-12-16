from ....datasources.meta import dicts, filters, frequencies
from ....util import NamedDict
from ...meta import aggregators


class Delta:
    def __init__(self, prefix, parent_revision, revision):

        # Datasources
        self.datasources = NamedDict()
        self.datasources.token_delta = frequencies.delta(
            parent_revision.datasources.token_frequency,
            revision.datasources.token_frequency,
            name=prefix + ".token_delta"
        )
        """
        A token frequency delta table
        """

        self.datasources.token_prop_delta = frequencies.prop_delta(
            parent_revision.datasources.token_frequency,
            self.datasources.token_delta,
            name=prefix + ".token_prop_delta"
        )
        """
        A token proportional frequency delta table
        """

        self.datasources.number_delta = frequencies.delta(
            parent_revision.datasources.number_frequency,
            revision.datasources.number_frequency,
            name=prefix + ".number_delta"
        )
        """
        A number frequency delta table
        """

        self.datasources.number_prop_delta = frequencies.prop_delta(
            parent_revision.datasources.number_frequency,
            self.datasources.number_delta,
            name=prefix + ".number_prop_delta"
        )
        """
        A number proportional frequency delta table
        """

        self.datasources.whitespace_delta = frequencies.delta(
            parent_revision.datasources.whitespace_frequency,
            revision.datasources.whitespace_frequency,
            name=prefix + ".whitespace_delta"
        )
        """
        A whitespace frequency delta table
        """

        self.datasources.whitespace_prop_delta = frequencies.prop_delta(
            parent_revision.datasources.whitespace_frequency,
            self.datasources.whitespace_delta,
            name=prefix + ".whitespace_prop_delta"
        )
        """
        A whitespace proportional frequency delta table
        """

        self.datasources.markup_delta = frequencies.delta(
            parent_revision.datasources.markup_frequency,
            revision.datasources.markup_frequency,
            name=prefix + ".markup_delta"
        )
        """
        A markup frequency delta table
        """

        self.datasources.markup_prop_delta = frequencies.prop_delta(
            parent_revision.datasources.markup_frequency,
            self.datasources.markup_delta,
            name=prefix + ".markup_prop_delta"
        )
        """
        A markup proportional frequency delta table
        """

        self.datasources.cjk_delta = frequencies.delta(
            parent_revision.datasources.cjk_frequency,
            revision.datasources.cjk_frequency,
            name=prefix + ".cjk_delta"
        )
        """
        A cjk frequency delta table
        """

        self.datasources.cjk_prop_delta = frequencies.prop_delta(
            parent_revision.datasources.cjk_frequency,
            self.datasources.cjk_delta,
            name=prefix + ".cjk_prop_delta"
        )
        """
        A cjk proportional frequency delta table
        """

        self.datasources.entity_delta = frequencies.delta(
            parent_revision.datasources.entity_frequency,
            revision.datasources.entity_frequency,
            name=prefix + ".entity_delta"
        )
        """
        A entity frequency delta table
        """

        self.datasources.entity_prop_delta = frequencies.prop_delta(
            parent_revision.datasources.entity_frequency,
            self.datasources.entity_delta,
            name=prefix + ".entity_prop_delta"
        )
        """
        A entity proportional frequency delta table
        """

        self.datasources.url_delta = frequencies.delta(
            parent_revision.datasources.url_frequency,
            revision.datasources.url_frequency,
            name=prefix + ".url_delta"
        )
        """
        A url frequency delta table
        """

        self.datasources.url_prop_delta = frequencies.prop_delta(
            parent_revision.datasources.url_frequency,
            self.datasources.url_delta,
            name=prefix + ".url_prop_delta"
        )
        """
        A url proportional frequency delta table
        """

        self.datasources.word_delta = frequencies.delta(
            parent_revision.datasources.word_frequency,
            revision.datasources.word_frequency,
            name=prefix + ".word_delta"
        )
        """
        A lower-cased word frequency delta table
        """

        self.datasources.word_prop_delta = frequencies.prop_delta(
            parent_revision.datasources.word_frequency,
            self.datasources.word_delta,
            name=prefix + ".word_prop_delta"
        )
        """
        A lower-cased word proportional frequency delta table
        """

        self.datasources.uppercase_word_delta = frequencies.delta(
            parent_revision.datasources.uppercase_word_frequency,
            revision.datasources.uppercase_word_frequency,
            name=prefix + ".uppercase_word_delta"
        )
        """
        A uppercase word frequency delta table
        """

        self.datasources.uppercase_word_prop_delta = frequencies.prop_delta(
            parent_revision.datasources.uppercase_word_frequency,
            self.datasources.uppercase_word_delta,
            name=prefix + ".uppercase_word_prop_delta"
        )
        """
        A uppercase word proportional frequency delta table
        """

        self.datasources.punctuation_delta = frequencies.delta(
            parent_revision.datasources.punctuation_frequency,
            revision.datasources.punctuation_frequency,
            name=prefix + ".punctuation_delta"
        )
        """
        A punctuation frequency delta table
        """

        self.datasources.punctuation_prop_delta = frequencies.prop_delta(
            parent_revision.datasources.punctuation_frequency,
            self.datasources.punctuation_delta,
            name=prefix + ".punctuation_prop_delta"
        )
        """
        A punctuation proportional frequency delta table
        """

        self.datasources.break_delta = frequencies.delta(
            parent_revision.datasources.break_frequency,
            revision.datasources.break_frequency,
            name=prefix + ".break_delta"
        )
        """
        A break frequency delta table
        """

        self.datasources.break_prop_delta = frequencies.prop_delta(
            parent_revision.datasources.break_frequency,
            self.datasources.break_delta,
            name=prefix + ".break_prop_delta"
        )
        """
        A break proportional frequency delta table
        """

        # Features

        self.token_delta_sum = aggregators.sum(
            dicts.values(self.datasources.token_delta),
            name=prefix + ".token_delta_sum"
        )
        """
        The sum of delta changes in the token frequency table
        """

        self.token_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.token_delta)),
            name=prefix + ".token_delta_increase"
        )
        """
        The sum of delta increases in the token frequency table
        """

        self.token_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.token_delta)),
            name=prefix + ".token_delta_decrease"
        )
        """
        The sum of delta decreases in the token frequency table
        """

        self.token_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.token_prop_delta),
            name=prefix + ".token_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the token frequency table
        """

        self.token_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.token_prop_delta)),
            name=prefix + ".token_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the token frequency table
        """

        self.token_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.token_prop_delta)),
            name=prefix + ".token_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the token frequency table
        """

        # number
        self.number_delta_sum = aggregators.sum(
            dicts.values(self.datasources.number_delta),
            name=prefix + ".number_delta_sum"
        )
        """
        The sum of delta changes in the number frequency table
        """

        self.number_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.number_delta)),
            name=prefix + ".number_delta_increase"
        )
        """
        The sum of delta increases in the number frequency table
        """

        self.number_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.number_delta)),
            name=prefix + ".number_delta_decrease"
        )
        """
        The sum of delta decreases in the number frequency table
        """

        self.number_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.number_prop_delta),
            name=prefix + ".number_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the number frequency table
        """

        self.number_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.number_prop_delta)),
            name=prefix + ".number_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the number frequency table
        """

        self.number_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.number_prop_delta)),
            name=prefix + ".number_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the number frequency table
        """

        # whitespace
        self.whitespace_delta_sum = aggregators.sum(
            dicts.values(self.datasources.whitespace_delta),
            name=prefix + ".whitespace_delta_sum"
        )
        """
        The sum of delta changes in the whitespace frequency table
        """

        self.whitespace_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.whitespace_delta)),
            name=prefix + ".whitespace_delta_increase"
        )
        """
        The sum of delta increases in the whitespace frequency table
        """

        self.whitespace_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.whitespace_delta)),
            name=prefix + ".whitespace_delta_decrease"
        )
        """
        The sum of delta decreases in the whitespace frequency table
        """

        self.whitespace_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.whitespace_prop_delta),
            name=prefix + ".whitespace_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the whitespace frequency table
        """

        self.whitespace_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.whitespace_prop_delta)),
            name=prefix + ".whitespace_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the whitespace frequency table
        """

        self.whitespace_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.whitespace_prop_delta)),
            name=prefix + ".whitespace_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the whitespace frequency table
        """

        # markup
        self.markup_delta_sum = aggregators.sum(
            dicts.values(self.datasources.markup_delta),
            name=prefix + ".markup_delta_sum"
        )
        """
        The sum of delta changes in the markup frequency table
        """

        self.markup_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.markup_delta)),
            name=prefix + ".markup_delta_increase"
        )
        """
        The sum of delta increases in the markup frequency table
        """

        self.markup_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.markup_delta)),
            name=prefix + ".markup_delta_decrease"
        )
        """
        The sum of delta decreases in the markup frequency table
        """

        self.markup_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.markup_prop_delta),
            name=prefix + ".markup_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the markup frequency table
        """

        self.markup_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.markup_prop_delta)),
            name=prefix + ".markup_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the markup frequency table
        """

        self.markup_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.markup_prop_delta)),
            name=prefix + ".markup_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the markup frequency table
        """

        # cjk
        self.cjk_delta_sum = aggregators.sum(
            dicts.values(self.datasources.cjk_delta),
            name=prefix + ".cjk_delta_sum"
        )
        """
        The sum of delta changes in the cjk frequency table
        """

        self.cjk_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.cjk_delta)),
            name=prefix + ".cjk_delta_increase"
        )
        """
        The sum of delta increases in the cjk frequency table
        """

        self.cjk_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.cjk_delta)),
            name=prefix + ".cjk_delta_decrease"
        )
        """
        The sum of delta decreases in the cjk frequency table
        """

        self.cjk_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.cjk_prop_delta),
            name=prefix + ".cjk_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the cjk frequency table
        """

        self.cjk_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.cjk_prop_delta)),
            name=prefix + ".cjk_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the cjk frequency table
        """

        self.cjk_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.cjk_prop_delta)),
            name=prefix + ".cjk_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the cjk frequency table
        """

        # entity
        self.entity_delta_sum = aggregators.sum(
            dicts.values(self.datasources.entity_delta),
            name=prefix + ".entity_delta_sum"
        )
        """
        The sum of delta changes in the entity frequency table
        """

        self.entity_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.entity_delta)),
            name=prefix + ".entity_delta_increase"
        )
        """
        The sum of delta increases in the entity frequency table
        """

        self.entity_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.entity_delta)),
            name=prefix + ".entity_delta_decrease"
        )
        """
        The sum of delta decreases in the entity frequency table
        """

        self.entity_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.entity_prop_delta),
            name=prefix + ".entity_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the entity frequency table
        """

        self.entity_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.entity_prop_delta)),
            name=prefix + ".entity_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the entity frequency table
        """

        self.entity_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.entity_prop_delta)),
            name=prefix + ".entity_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the entity frequency table
        """

        # url
        self.url_delta_sum = aggregators.sum(
            dicts.values(self.datasources.url_delta),
            name=prefix + ".url_delta_sum"
        )
        """
        The sum of delta changes in the url frequency table
        """

        self.url_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.url_delta)),
            name=prefix + ".url_delta_increase"
        )
        """
        The sum of delta increases in the url frequency table
        """

        self.url_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.url_delta)),
            name=prefix + ".url_delta_decrease"
        )
        """
        The sum of delta decreases in the url frequency table
        """

        self.url_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.url_prop_delta),
            name=prefix + ".url_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the url frequency table
        """

        self.url_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.url_prop_delta)),
            name=prefix + ".url_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the url frequency table
        """

        self.url_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.url_prop_delta)),
            name=prefix + ".url_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the url frequency table
        """

        # word
        self.word_delta_sum = aggregators.sum(
            dicts.values(self.datasources.word_delta),
            name=prefix + ".word_delta_sum"
        )
        """
        The sum of delta changes in the word frequency table
        """

        self.word_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.word_delta)),
            name=prefix + ".word_delta_increase"
        )
        """
        The sum of delta increases in the word frequency table
        """

        self.word_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.word_delta)),
            name=prefix + ".word_delta_decrease"
        )
        """
        The sum of delta decreases in the word frequency table
        """

        self.word_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.word_prop_delta),
            name=prefix + ".word_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the word frequency table
        """

        self.word_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.word_prop_delta)),
            name=prefix + ".word_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the word frequency table
        """

        self.word_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.word_prop_delta)),
            name=prefix + ".word_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the word frequency table
        """

        # punctuation
        self.punctuation_delta_sum = aggregators.sum(
            dicts.values(self.datasources.punctuation_delta),
            name=prefix + ".punctuation_delta_sum"
        )
        """
        The sum of delta changes in the punctuation frequency table
        """

        self.punctuation_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.punctuation_delta)),
            name=prefix + ".punctuation_delta_increase"
        )
        """
        The sum of delta increases in the punctuation frequency table
        """

        self.punctuation_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.punctuation_delta)),
            name=prefix + ".punctuation_delta_decrease"
        )
        """
        The sum of delta decreases in the punctuation frequency table
        """

        self.punctuation_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.punctuation_prop_delta),
            name=prefix + ".punctuation_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the punctuation frequency table
        """

        self.punctuation_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.punctuation_prop_delta)),
            name=prefix + ".punctuation_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the punctuation frequency table
        """

        self.punctuation_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.punctuation_prop_delta)),
            name=prefix + ".punctuation_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the punctuation frequency table
        """

        # break
        self.break_delta_sum = aggregators.sum(
            dicts.values(self.datasources.break_delta),
            name=prefix + ".break_delta_sum"
        )
        """
        The sum of delta changes in the break frequency table
        """

        self.break_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.break_delta)),
            name=prefix + ".break_delta_increase"
        )
        """
        The sum of delta increases in the break frequency table
        """

        self.break_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.break_delta)),
            name=prefix + ".break_delta_decrease"
        )
        """
        The sum of delta decreases in the break frequency table
        """

        self.break_prop_delta_sum = aggregators.sum(
            dicts.values(self.datasources.break_prop_delta),
            name=prefix + ".break_prop_delta_sum"
        )
        """
        The sum of proportional delta changes in the break frequency table
        """

        self.break_prop_delta_increase = aggregators.sum(
            filters.positive(dicts.values(self.datasources.break_prop_delta)),
            name=prefix + ".break_prop_delta_increase"
        )
        """
        The sum of proportional delta increases in the break frequency table
        """

        self.break_prop_delta_decrease = aggregators.sum(
            filters.negative(dicts.values(self.datasources.break_prop_delta)),
            name=prefix + ".break_prop_delta_decrease"
        )
        """
        The sum of proportional delta decreases in the break frequency table
        """
