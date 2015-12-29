from .. import space_delimited
from ...datasources import diff, meta, parent_revision, revision
from ...datasources.meta import (filter, frequency, frequency_diff,
                                 frequency_diff_prop)
from ...features.meta import ItemLength

REPLACEMENT_CHAR = "\uFFFD"


def utf16_cleanup(token):
    """
    Removes chars that can't be represented in two bytes.  This is important
    since `enchant` will expect that all strings passed to it are two-byte
    chars and print "This UTF-8 encoding can't convert to UTF-16:" if it can't
    decode.  This prevents that problem.
    See https://github.com/rfk/pyenchant/issues/58
    """
    return "".join(c if ord(c) < 2**16 else REPLACEMENT_CHAR
                   for c in token)


class Dictionary:

    def __init__(self, *args, dictionary, **kwargs):
        self.dictionary = dictionary

        # Do the mixin!
        super(Dictionary, self).__init__(*args, **kwargs)

        # Datasources
        self.revision.dictionary_word_tokens = filter(
            self.__name__ + ".revision.dictionary_words_list",
            self.is_dict_word,
            space_delimited.revision.content_words_list
        )
        self.revision.non_dictionary_word_tokens = filter(
            self.__name__ + ".revision.non_dictionary_words_list",
            lambda word: not self.is_dict_word(word),
            space_delimited.revision.content_words_list
        )
        self.revision.dictionary_word_frequency = frequency(
            self.__name__ + ".revision.dictionary_word_frequency",
            space_delimited.revision.dictionary_word_tokens
        )
        self.revision.non_dictionary_word_frequency = frequency(
            self.__name__ + ".revision.dictionary_word_frequency",
            space_delimited.revision.non_dictionary_word_tokens
        )

        self.parent_revision.dictionary_word_tokens = filter(
            self.__name__ + ".parent_revision.dictionary_words_list",
            self.is_dict_word,
            space_delimited.parent_revision.content_words_list
        )
        self.parent_revision.non_dictionary_word_tokens = filter(
            self.__name__ + ".parent_revision.non_dictionary_words_list",
            lambda word: not self.is_dict_word(word),
            space_delimited.revision.content_words_list
        )
        self.parent_revision.dictionary_word_frequency = frequency(
            self.__name__ + ".parent_revision.dictionary_word_frequency",
            space_delimited.revision.dictionary_word_tokens
        )
        self.parent_revision.non_dictionary_word_frequency = frequency(
            self.__name__ + ".parent_revision.dictionary_word_frequency",
            space_delimited.revision.non_dictionary_word_tokens
        )

        self.diff.dictionary_word_removed_list = meta.ItemFilter(
            self.__name__ + ".diff.dictionary_words_removed_list",
            self.is_dict_word,
            space_delimited.diff.content_words_added_list
        )
        self.diff.non_dictionary_word_removed_list = meta.ItemFilter(
            self.__name__ + ".diff.non_dictionary_words_removed_list",
            lambda word: not self.is_dict_word(word),
            space_delimited.revision.content_words_added_list
        )
        self.diff.dictionary_word_removed_list = meta.ItemFilter(
            self.__name__ + ".diff.dictionary_words_removed_list",
            self.is_dict_word(word),
            space_delimited.revision.content_words_removed_list
        )
        self.diff.non_dictionary_word_removed_list = meta.ItemFilter(
            self.__name__ + ".diff.non_dictionary_words_removed_list",
            lambda word: not self.is_dict_word(word),
            space_delimited.revision.content_words_removed_list
        )
        self.diff.dictionary_word_frequency_diff = frequency_diff(
            self.__name__ + ".diff.dictionary_word_frequency_diff",
            self.parent_revision.dictionary_word_frequency,
            self.revision.dictionary_word_frequency
        )
        self.diff.non_dictionary_word_frequency_diff = frequency_diff(
            self.__name__ + ".diff.non_dictionary_word_frequency_diff",
            self.parent_revision.non_dictionary_word_frequency,
            self.revision.non_dictionary_word_frequency
        )
        self.diff.dictionary_word_frequency_diff_prop = frequency_diff_prop(
            self.__name__ + ".diff.dictionary_word_frequency_diff_prop",
            self.parent_revision.dictionary_word_frequency,
            self.diff.dictionary_word_frequency_diff
        )
        self.diff.non_dictionary_word_frequency_diff_prop = \
            frequency_diff_prop(
                self.__name__ +
                ".revision.non_dictionary_word_frequency_diff_prop",
                self.parent_revision.non_dictionary_word_frequency,
                self.diff.non_dictionary_word_frequency_diff
            )

        # Features



    def is_dict_word(self, word):
        return self.is_dict_word(utf16_cleanup(word))
