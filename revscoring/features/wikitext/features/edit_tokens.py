from ....datasources.meta import mappers
from ...meta import aggregators


class Diff:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.segments_added = aggregators.len(
            self.datasources.segments_added,
            name=self._name + ".segments_added"
        )
        """
        A count of the number of segments added in this edit.
        """

        self.segments_removed = aggregators.len(
            self.datasources.segments_removed,
            name=self._name + ".segments_removed"
        )
        """
        A count of the number of segments removed in this edit.
        """

        self.tokens_added = aggregators.len(
            self.datasources.tokens_added,
            name=self._name + ".tokens_added"
        )
        """
        A count of the tokens added in this edit.
        """

        self.tokens_removed = aggregators.len(
            self.datasources.tokens_removed,
            name=self._name + ".tokens_removed"
        )
        """
        A count of the tokens removed in this edit.
        """

        self.numbers_added = aggregators.len(
            self.datasources.numbers_added,
            name=self._name + ".numbers_added"
        )
        """
        A count of the number tokens added in this edit.
        """

        self.numbers_removed = aggregators.len(
            self.datasources.numbers_removed,
            name=self._name + ".numbers_removed"
        )
        """
        A count of the number tokens removed in this edit.
        """

        self.markups_added = aggregators.len(
            self.datasources.markups_added,
            name=self._name + ".markups_added"
        )
        """
        A count of the markup tokens added in this edit.
        """

        self.markups_removed = aggregators.len(
            self.datasources.markups_removed,
            name=self._name + ".markups_removed"
        )
        """
        A count of the markup tokens removed in this edit.
        """

        self.whitespaces_added = aggregators.len(
            self.datasources.whitespaces_added,
            name=self._name + ".whitespaces_added"
        )
        """
        A count of the whitespace tokens added in this edit.
        """

        self.whitespaces_removed = aggregators.len(
            self.datasources.whitespaces_removed,
            name=self._name + ".whitespaces_removed"
        )
        """
        A count of the whitespace tokens removed in this edit.
        """

        self.cjks_added = aggregators.len(
            self.datasources.cjks_added,
            name=self._name + ".cjks_added"
        )
        """
        A count of the cjk tokens added in this edit.
        """

        self.cjks_removed = aggregators.len(
            self.datasources.cjks_removed,
            name=self._name + ".cjks_removed"
        )
        """
        A count of the cjk tokens removed in this edit.
        """

        self.entities_added = aggregators.len(
            self.datasources.entities_added,
            name=self._name + ".entities_added"
        )
        """
        A count of the entity tokens added in this edit.
        """

        self.entities_removed = aggregators.len(
            self.datasources.entities_removed,
            name=self._name + ".entities_removed"
        )
        """
        A count of the entity tokens removed in this edit.
        """

        self.urls_added = aggregators.len(
            self.datasources.urls_added,
            name=self._name + ".urls_added"
        )
        """
        A count of the url tokens added in this edit.
        """

        self.urls_removed = aggregators.len(
            self.datasources.urls_removed,
            name=self._name + ".urls_removed"
        )
        """
        A count of the url tokens removed in this edit.
        """

        self.words_added = aggregators.len(
            self.datasources.words_added,
            name=self._name + ".words_added"
        )
        """
        A count of the word tokens added in this edit.
        """

        self.words_removed = aggregators.len(
            self.datasources.words_removed,
            name=self._name + ".words_removed"
        )
        """
        A count of the word tokens removed in this edit.
        """

        self.uppercase_words_added = aggregators.len(
            self.datasources.uppercase_words_added,
            name=self._name + ".words_added"
        )
        """
        A count of the word tokens added in this edit.
        """

        self.uppercase_words_removed = aggregators.len(
            self.datasources.uppercase_words_removed,
            name=self._name + ".words_removed"
        )
        """
        A count of the word tokens removed in this edit.
        """

        self.punctuations_added = aggregators.len(
            self.datasources.punctuations_added,
            name=self._name + ".punctuations_added"
        )
        """
        A count of the punctuation tokens added in this edit.
        """

        self.punctuations_removed = aggregators.len(
            self.datasources.punctuations_removed,
            name=self._name + ".punctuations_removed"
        )
        """
        A count of the punctuation tokens removed in this edit.
        """

        self.breaks_added = aggregators.len(
            self.datasources.breaks_added,
            name=self._name + ".breaks_added"
        )
        """
        A count of the break tokens added in this edit.
        """

        self.breaks_removed = aggregators.len(
            self.datasources.breaks_removed,
            name=self._name + ".breaks_removed"
        )
        """
        A count of the break tokens removed in this edit.
        """

        self.longest_token_added = aggregators.max(
            mappers.map(len, self.datasources.tokens_added),
            name=self._name + '.longest_token_added'
        )
        """
        The length of the longest token added in the edit
        """

        self.longest_uppercase_word_added = aggregators.max(
            mappers.map(len, self.datasources.uppercase_words_added)
        )
        """
        The length of the longest sequence of UPPPERCASE characters added in
        the edit
        """
