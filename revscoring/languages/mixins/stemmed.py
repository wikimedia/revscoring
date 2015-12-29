from ...datasources import diff, parent_revision, revision
from ...datasources.meta import ItemMapper, TokenFrequency
from ...features.meta import ItemLength
from ..common.space_delimited import diff as sd_diff
from ..common.space_delimited import parent_revision as sd_parent_revision
from ..common.space_delimited import revision as sd_revision


class Stemmed:

    def __init__(self, *args, stem, **kwargs):
        self.stem = stem

        # Do the mixin!
        super(Stemmed, self).__init__(*args, **kwargs)

        # Datasources
        self.revision.stemmed_word_tokens = ItemMapper(
            self.__name__ + ".revision.stemmed_word_tokens",
            sd_revision.words,
            self.stem
        )
        """
        Generates a list of stemmed word tokens
        """

        self.revision.stemmed_word_frequency = TokenFrequency(
            self.__name__ + ".revision.stemmed_word_frequency",
            self.revision.stemmed_words
        )
        """
        Generates a dict of stemmed word counts
        """

        self.revision.stemmed_content_word_tokens = ItemMapper(
            self.__name__ + ".revision.stemmed_content_word_tokens",
            sd_revision.content_words,
            self.stem
        )
        """
        Generates a list of stemmed content word tokens
        """

        self.revision.stemmed_content_word_frequency = TokenFrequency(
            self.__name__ + ".revision.stemmed_content_word_frequency",
            self.revision.stemmed_content_words
        )
        """
        Generates a dict of stemmed content word counts
        """

        self.parent_revision.stemmed_word_tokens = ItemMapper(
            self.__name__ + ".parent_revision.stemmed_word_tokens",
            sd_parent_revision.words,
            self.stem
        )
        """
        Generates a list of stemmed word tokens
        """

        self.parent_revision.stemmed_word_frequency = TokenFrequency(
            self.__name__ + ".parent_revision.stemmed_word_frequency",
            self.parent_revision.stemmed_words
        )
        """
        Generates a dict of stemmed word counts
        """

        self.parent_revision.stemmed_content_word_tokens = ItemMapper(
            self.__name__ + ".parent_revision.stemmed_content_word_tokens",
            sd_parent_revision.content_words,
            self.stem
        )
        """
        Generates a list of stemmed content word tokens
        """

        self.parent_revision.stemmed_content_word_frequency = TokenFrequency(
            self.__name__ + ".parent_revision.stemmed_content_word_frequency",
            self.parent_revision.stemmed_content_words
        )
        """
        Generates a dict of stemmed content word counts
        """

        self.diff.stemmed_word_tokens_added = ItemMapper(
            self.__name__ + ".diff.stemmed_word_tokens_added",
            sd_diff.word_tokens_added,
            self.stem
        )
        """
        Generates a list of stemmed word tokens added
        """

        self.diff.stemmed_word_tokens_removed = ItemMapper(
            self.__name__ + ".diff.stemmed_word_tokens_removed",
            sd_diff.word_tokens_removed,
            self.stem
        )
        """
        Generates a list of stemmed word tokens added
        """

        self.diff.stemmed_content_word_tokens_added = ItemMapper(
            self.__name__ + ".diff.stemmed_content_word_tokens_added",
            sd_diff.content_word_tokens_added,
            self.stem
        )
        """
        Generates a list of stemmed word tokens added
        """

        self.diff.stemmed_content_word_tokens_removed = ItemMapper(
            self.__name__ + ".diff.stemmed_content_word_tokens_removed",
            sd_diff.content_word_tokens_removed,
            self.stem
        )
        """
        Generates a list of stemmed word tokens added
        """

        self.diff.stemmed_word_frequency_diff = \
            TokenFrequencyDiff(
                self.__name__ + ".diff.stemmed_word_frequency_diff"
                self.parent_revision.stemmed_content_word_frequency,
                self.revision.stemmed_content_word_frequency
            )

        self.diff.stemmed_content_word_frequency_diff = \
            TokenFrequencyDiff(
                self.__name__ +
                ".diff.stemmed_content_word_frequency_diff"
                self.parent_revision.stemmed_content_word_frequency,
                self.revision.stemmed_content_word_frequency
            )

        # Features
        self.revision.stemmed_word_length
        self.revision.stemmed_content_word_length

        self.parent_revision.stemmed_word_length
        self.parent_revision.stemmed_content_word_length

        self.diff.stemmed_word_proportional_frequency_change = \
            TokenFrequencySum(
                self.__name__ +
                ".diff.stemmed_word_proportional_frequency_change",
                self.diff.stemmed_word_proportional_frequency_diff
            )
        self.diff.stemmed_word_proportional_frequency_increase = \
            TokenFrequencyIncrease(
                self.__name__ +
                ".diff.stemmed_word_proportional_frequency_increase",
                self.diff.stemmed_word_proportional_frequency_diff
            )
        self.diff.stemmed_word_proportional_frequency_decrease = \
            TokenFrequencyDecrease(
                self.__name__ +
                ".diff.stemmed_word_proportional_frequency_decrease",
                self.diff.stemmed_word_proportional_frequency_diff
            )
