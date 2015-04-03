import re
from itertools import groupby

from . import modifiers, parent_revision, revision
from ..datasources import diff
from ..languages import is_badword, is_misspelled
from .feature import Feature
from .util import MARKUP_RE, NUMERIC_RE, SYMBOLIC_RE

bytes_changed = revision.bytes - parent_revision.bytes

bytes_changed_ratio = bytes_changed / modifiers.max(parent_revision.bytes, 1)


def process_segments_added(diff_added_segments):
    return len(diff_added_segments)

segments_added = Feature("diff.segments_added", process_segments_added,
                         returns=int, depends_on=[diff.added_segments])

def process_segment_removed(diff_segments_removed):
    return len(diff_segments_removed)

segments_removed = Feature("segments_removed", process_segment_removed,
                           returns=int, depends_on=[diff.removed_segments])

############################## Characters ######################################

def process_chars_added(diff_added_segments):
    return len("".join(diff_added_segments))

chars_added = Feature("diff.chars_added", process_chars_added,
                      returns=int, depends_on=[diff.added_segments])

def process_chars_removed(diff_removed_segments):
    return len("".join(diff_removed_segments))

chars_removed = Feature("diff.chars_removed", process_chars_removed,
                        returns=int, depends_on=[diff.removed_segments])

proportion_of_chars_removed = chars_removed / \
              modifiers.max(parent_revision.chars, 1)
proportion_of_chars_added = chars_removed / \
            modifiers.max(revision.chars, 1)

def process_markup_chars_added(diff_added_segments):
    concat = "".join(diff_added_segments)
    return sum(len(m.group(0)) for m in MARKUP_RE.finditer(concat))

markup_chars_added = \
        Feature("diff.markup_chars_added", process_markup_chars_added,
                returns=int, depends_on=[diff.added_segments])

def process_markup_chars_removed(diff_removed_segments):
    concat = "".join(diff_removed_segments)
    return sum(len(m.group(0)) for m in MARKUP_RE.finditer(concat))

markup_chars_removed = \
        Feature("diff.markup_chars_removed", process_markup_chars_removed,
                returns=int, depends_on=[diff.removed_segments])

proportion_of_markup_chars_added = \
        markup_chars_added / modifiers.max(chars_added, 1)
added_markup_chars_ratio = \
        proportion_of_markup_chars_added / \
        modifiers.max(parent_revision.proportion_of_markup_chars, 1)

def process_numeric_chars_added(diff_added_segments):
    concat = "".join(diff_added_segments)
    return sum(len(m.group(0)) for m in NUMERIC_RE.finditer(concat))

numeric_chars_added = \
        Feature("diff.numeric_chars_added", process_numeric_chars_added,
                returns=int, depends_on=[diff.added_segments])

def process_numeric_chars_removed(diff_removed_segments):
    concat = "".join(diff_removed_segments)
    return sum(len(m.group(0)) for m in NUMERIC_RE.finditer(concat))

numeric_chars_removed = \
        Feature("diff.numeric_chars_removed", process_numeric_chars_removed,
                returns=int, depends_on=[diff.removed_segments])

proportion_of_numeric_chars_added = \
    numeric_chars_added / modifiers.max(chars_added, 1)
added_number_chars_ratio = \
        proportion_of_numeric_chars_added / \
        modifiers.max(parent_revision.proportion_of_numeric_chars, 1)

def process_symbolic_chars_added(diff_added_segments):
    concat = "".join(diff_added_segments)
    return sum(len(m.group(0)) for m in SYMBOLIC_RE.finditer(concat))

symbolic_chars_added = \
        Feature("diff.symbolic_chars_added", process_symbolic_chars_added,
                returns=int, depends_on=[diff.added_segments])

def process_symbolic_chars_removed(diff_removed_segments):
    concat = "".join(diff_removed_segments)
    return sum(len(m.group(0)) for m in SYMBOLIC_RE.finditer(concat))

symbolic_chars_removed = \
        Feature("diff.symbolic_chars_removed", process_symbolic_chars_removed,
                returns=int, depends_on=[diff.removed_segments])

proportion_of_symbolic_chars_added = symbolic_chars_added / modifiers.max(chars_added, 1)
added_symbolic_chars_ratio = \
        proportion_of_symbolic_chars_added / \
        modifiers.max(parent_revision.proportion_of_symbolic_chars, 1)

def process_uppercase_chars_added(diff_added_segments):
    return sum((not c.lower() == c) for segment in diff_added_segments
                                    for c in segment)

uppercase_chars_added = \
        Feature("diff.uppercase_chars_added", process_uppercase_chars_added,
                returns=int, depends_on=[diff.added_segments])

def process_uppercase_chars_removed(diff_removed_segments):
    return sum((not c.lower() == c) for segment in diff_removed_segments
                                    for c in segment)

uppercase_chars_removed = \
        Feature("diff.uppercase_chars_removed", process_uppercase_chars_removed,
                returns=int, depends_on=[diff.removed_segments])

proportion_of_uppercase_chars_added = \
    uppercase_chars_added / modifiers.max(chars_added, 1)
added_uppercase_chars_ratio = \
        proportion_of_uppercase_chars_added / \
        modifiers.max(parent_revision.proportion_of_uppercase_chars, 1)

def process_longest_repeated_char_added(diff_added_segments):
    try:
        return max(sum(1 for _ in group)
                   for segment in diff_added_segments
                   for _, group in groupby(segment.lower()))
    except ValueError:
        # Happens when there's no segments added
        return 1

longest_repeated_char_added = \
        Feature("diff.longest_repeated_char_added",
                process_longest_repeated_char_added,
                returns=int, depends_on=[diff.added_segments])

############################### Words ##########################################

def process_words_added(diff_added_words):
    return len(diff_added_words)

words_added = Feature("diff.words_added", process_words_added,
                      returns=int, depends_on=[diff.added_words])

def process_words_removed(diff_removed_words):
    return len(diff_removed_words)

words_removed = Feature("diff.words_removed", process_words_removed,
                        returns=int, depends_on=[diff.removed_words])

def process_badwords_added(is_badword, diff_added_words):
    return sum(is_badword(word) for word in diff_added_words)

badwords_added = Feature("diff.badwords_added", process_badwords_added,
                         returns=int, depends_on=[is_badword, diff.added_words])

proportion_of_badwords_added = badwords_added / modifiers.max(words_added, 1)
added_badwords_ratio = proportion_of_badwords_added / \
                       modifiers.max(parent_revision.proportion_of_badwords, 1)

def process_badwords_removed(is_badword, diff_removed_words):
   return sum(is_badword(word) for word in diff_removed_words)

badwords_removed = Feature("diff.badwords_removed", process_badwords_removed,
                           returns=int,
                           depends_on=[is_badword, diff.removed_words])

proportion_of_badwords_removed = badwords_removed / modifiers.max(words_added, 1)
removed_badwords_ratio = proportion_of_badwords_removed / \
                         modifiers.max(parent_revision.proportion_of_badwords, 1)

def process_misspellings_added(is_misspelled, diff_added_words):
    return sum(is_misspelled(word) for word in diff_added_words)

misspellings_added = \
    Feature("diff.misspellings_added", process_misspellings_added,
            returns=int, depends_on=[is_misspelled, diff.added_words])

proportion_of_misspellings_added = \
        misspellings_added / modifiers.max(words_added, 1)
added_misspellings_ratio = \
        proportion_of_misspellings_added / \
        modifiers.max(parent_revision.proportion_of_misspellings, 1)

def process_misspellings_removed(is_misspelled, diff_removed_words):
    return sum(is_misspelled(word) for word in diff_removed_words)

misspellings_removed = \
        Feature("diff.misspellings_removed", process_misspellings_removed,
                returns=int, depends_on=[is_misspelled, diff.removed_words])

proportion_of_misspellings_removed = \
        misspellings_removed / modifiers.max(words_removed, 1)
removed_misspellings_ratio = \
        proportion_of_misspellings_removed / \
        modifiers.max(parent_revision.proportion_of_misspellings, 1)

############################## tokens ##########################################

def process_longest_token_added(diff_added_tokens):
    try:
        return max(len(token) for token in diff_added_tokens)
    except ValueError:
        # Happens when there's no tokens added
        return 1

longest_token_added = \
        Feature("diff.longest_token_added", process_longest_token_added,
                returns=int, depends_on=[diff.added_tokens])
