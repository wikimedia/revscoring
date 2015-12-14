class Diff:
    def __init__(self, prefix, parent_revision, revision):

        self.token_delta = frequencies.delta(
            parent_revision.token_fequency, revision.token_fequency,
            name=prefix + ".token_delta"
        )
        """
        A token frequency delta table
        """

        self.token_prop_delta = frequencies.prop_delta(
            parent_revision.token_fequency, self.token_delta,
            name=prefix + ".token_prop_delta"
        )
        """
        A token proportional frequency delta table
        """

        self.number_delta = frequencies.delta(
            parent_revision.number_frequency, revision.number_frequency,
            name=prefix + ".number_delta"
        )
        """
        A number frequency delta table
        """

        self.number_prop_delta = frequencies.prop_delta(
            parent_revision.number_fequency, self.number_delta,
            name=prefix + ".number_prop_delta"
        )
        """
        A number proportional frequency delta table
        """

        # whitespace
        self.whitespace_delta = frequencies.delta(
            parent_revision.whitespace_frequency, revision.whitespace_frequency,
            name=prefix + ".whitespace_delta"
        )
        """
        A whitespace frequency delta table
        """

        self.whitespace_prop_delta = frequencies.prop_delta(
            parent_revision.whitespace_fequency, self.whitespace_delta,
            name=prefix + ".whitespace_prop_delta"
        )
        """
        A whitespace proportional frequency delta table
        """

        # markup
        self.markup_delta = frequencies.delta(
            parent_revision.markup_frequency, revision.markup_frequency,
            name=prefix + ".markup_delta"
        )
        """
        A markup frequency delta table
        """

        self.markup_prop_delta = frequencies.prop_delta(
            parent_revision.markup_fequency, self.markup_delta,
            name=prefix + ".markup_prop_delta"
        )
        """
        A markup proportional frequency delta table
        """

        # cjk
        self.cjk_delta = frequencies.delta(
            parent_revision.cjk_frequency, revision.cjk_frequency,
            name=prefix + ".cjk_delta"
        )
        """
        A cjk frequency delta table
        """

        self.cjk_prop_delta = frequencies.prop_delta(
            parent_revision.cjk_fequency, self.cjk_delta,
            name=prefix + ".cjk_prop_delta"
        )
        """
        A cjk proportional frequency delta table
        """

        # entity
        self.entity_delta = frequencies.delta(
            parent_revision.entity_frequency, revision.entity_frequency,
            name=prefix + ".entity_delta"
        )
        """
        A entity frequency delta table
        """

        self.entity_prop_delta = frequencies.prop_delta(
            parent_revision.entity_fequency, self.entity_delta,
            name=prefix + ".entity_prop_delta"
        )
        """
        A entity proportional frequency delta table
        """

        # url
        self.url_delta = frequencies.delta(
            parent_revision.url_frequency, revision.url_frequency,
            name=prefix + ".url_delta"
        )
        """
        A url frequency delta table
        """

        self.url_prop_delta = frequencies.prop_delta(
            parent_revision.url_fequency, self.url_delta,
            name=prefix + ".url_prop_delta"
        )
        """
        A url proportional frequency delta table
        """

        # word
        self.word_delta = frequencies.delta(
            parent_revision.word_frequency, revision.word_frequency,
            name=prefix + ".word_delta"
        )
        """
        A word frequency delta table
        """

        self.word_prop_delta = frequencies.prop_delta(
            parent_revision.word_fequency, self.word_delta,
            name=prefix + ".word_prop_delta"
        )
        """
        A word proportional frequency delta table
        """

        # delta
        self.delta_delta = frequencies.delta(
            parent_revision.delta_frequency, revision.delta_frequency,
            name=prefix + ".delta_delta"
        )
        """
        A delta frequency delta table
        """

        self.delta_prop_delta = frequencies.prop_delta(
            parent_revision.delta_fequency, self.delta_delta,
            name=prefix + ".delta_prop_delta"
        )
        """
        A delta proportional frequency delta table
        """

        # break
        self.break_delta = frequencies.delta(
            parent_revision.break_frequency, revision.break_frequency,
            name=prefix + ".break_delta"
        )
        """
        A break frequency delta table
        """

        self.break_prop_delta = frequencies.prop_delta(
            parent_revision.break_fequency, self.break_delta,
            name=prefix + ".break_prop_delta"
        )
        """
        A break proportional frequency delta table
        """
