from revscoring.datasources.meta import mappers

from ...meta import aggregators


class Diff:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.segments_added = aggregators.len(
            self.datasources.segments_added,
            name=self._name + ".segments_added"
        )
        "`int` : The number of segments added "

        self.segments_removed = aggregators.len(
            self.datasources.segments_removed,
            name=self._name + ".segments_removed"
        )
        "`int` : The number of segments removed "

        self.tokens_added = aggregators.len(
            self.datasources.tokens_added,
            name=self._name + ".tokens_added"
        )
        "`int` : The number of tokens added "

        self.tokens_removed = aggregators.len(
            self.datasources.tokens_removed,
            name=self._name + ".tokens_removed"
        )
        "`int` : The number of tokens removed "

        self.numbers_added = aggregators.len(
            self.datasources.numbers_added,
            name=self._name + ".numbers_added"
        )
        "`int` : The number of number tokens added "

        self.numbers_removed = aggregators.len(
            self.datasources.numbers_removed,
            name=self._name + ".numbers_removed"
        )
        "`int` : The number of number tokens removed "

        self.markups_added = aggregators.len(
            self.datasources.markups_added,
            name=self._name + ".markups_added"
        )
        "`int` : The number of markup tokens added "

        self.markups_removed = aggregators.len(
            self.datasources.markups_removed,
            name=self._name + ".markups_removed"
        )
        "`int` : The number of markup tokens removed "

        self.whitespaces_added = aggregators.len(
            self.datasources.whitespaces_added,
            name=self._name + ".whitespaces_added"
        )
        "`int` : The number of whitespace tokens added "

        self.whitespaces_removed = aggregators.len(
            self.datasources.whitespaces_removed,
            name=self._name + ".whitespaces_removed"
        )
        "`int` : The number of whitespace tokens removed "

        self.cjks_added = aggregators.len(
            self.datasources.cjks_added,
            name=self._name + ".cjks_added"
        )
        "`int` : The number of cjk tokens added "

        self.cjks_removed = aggregators.len(
            self.datasources.cjks_removed,
            name=self._name + ".cjks_removed"
        )
        "`int` : The number of cjk tokens removed "

        self.entities_added = aggregators.len(
            self.datasources.entities_added,
            name=self._name + ".entities_added"
        )
        "`int` : The number of entity tokens added "

        self.entities_removed = aggregators.len(
            self.datasources.entities_removed,
            name=self._name + ".entities_removed"
        )
        "`int` : The number of entity tokens removed "

        self.urls_added = aggregators.len(
            self.datasources.urls_added,
            name=self._name + ".urls_added"
        )
        "`int` : The number of url tokens added "

        self.urls_removed = aggregators.len(
            self.datasources.urls_removed,
            name=self._name + ".urls_removed"
        )
        "`int` : The number of url tokens removed "

        self.words_added = aggregators.len(
            self.datasources.words_added,
            name=self._name + ".words_added"
        )
        "`int` : The number of word tokens added "

        self.words_removed = aggregators.len(
            self.datasources.words_removed,
            name=self._name + ".words_removed"
        )
        "`int` : The number of word tokens removed "

        self.uppercase_words_added = aggregators.len(
            self.datasources.uppercase_words_added,
            name=self._name + ".uppercase_words_added"
        )
        "`int` : The number of word tokens added "

        self.uppercase_words_removed = aggregators.len(
            self.datasources.uppercase_words_removed,
            name=self._name + ".uppercase_words_removed"
        )
        "`int` : The number of word tokens removed "

        self.punctuations_added = aggregators.len(
            self.datasources.punctuations_added,
            name=self._name + ".punctuations_added"
        )
        "`int` : The number of punctuation tokens added "

        self.punctuations_removed = aggregators.len(
            self.datasources.punctuations_removed,
            name=self._name + ".punctuations_removed"
        )
        "`int` : The number of punctuation tokens removed "

        self.breaks_added = aggregators.len(
            self.datasources.breaks_added,
            name=self._name + ".breaks_added"
        )
        "`int` : The number of break tokens added "

        self.breaks_removed = aggregators.len(
            self.datasources.breaks_removed,
            name=self._name + ".breaks_removed"
        )
        "`int` : The number of break tokens removed"

        self.longest_token_added = aggregators.max(
            mappers.map(len, self.datasources.tokens_added),
            name=self._name + '.longest_token_added'
        )
        "`int` : The length of the longest token added"

        self.longest_uppercase_word_added = aggregators.max(
            mappers.map(len, self.datasources.uppercase_words_added)
        )
        """
        `int` : The length of the longest sequence of UPPPERCASE characters
        added
        """
