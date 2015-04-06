from . import modifiers
from ..datasources import parent_revision, revision
from ..languages import is_badword, is_misspelled
from .feature import Feature
from .revision import bytes as revision_bytes
from .util import MARKUP_RE, NUMERIC_RE, SYMBOLIC_RE


################################## Bytes #######################################

def process_bytes(parent_revision_metadata):
    return parent_revision_metadata.bytes \
           if parent_revision_metadata is not None else 0

bytes = Feature("parent_revision.bytes", process_bytes,
                returns=int, depends_on=[parent_revision.metadata])

def process_was_same_user(parent_revision_metadata, revision_metadata):

    parent_user_id = parent_revision_metadata.user_id \
                     if parent_revision_metadata is not None else None
    parent_user_text = parent_revision_metadata.user_text \
                       if parent_revision_metadata is not None else None

    return (parent_user_id is not None and
            parent_user_id == revision_metadata.user_id) or \
           (parent_user_text is not None and
            parent_user_text == revision_metadata.user_text)

was_same_user = Feature("parent_revision.was_same_user", process_was_same_user,
                        returns=bool,
                        depends_on=[parent_revision.metadata,
                                    revision.metadata])

def process_seconds_since(parent_revision_metadata, revision_metadata):

    revision_timestamp = revision_metadata.timestamp \
                         if revision_metadata is not None else Timestamp(0)
    previous_timestamp = parent_revision_metadata.timestamp \
                         if parent_revision_metadata is not None and \
                            parent_revision_metadata.timestamp is not None \
                         else revision_timestamp

    return revision_timestamp - previous_timestamp

seconds_since = Feature("parent_revision.seconds_since", process_seconds_since,
                        returns=int,
                        depends_on=[parent_revision.metadata,
                                    revision.metadata])

################################# Characters ###################################

def process_chars(parent_revision_text):
    return len(parent_revision_text or "")

chars = Feature("parent_revision.chars", process_chars,
                returns=int, depends_on=[parent_revision.text])

def process_markup_chars(parent_revision_text):
    parent_revision_text = parent_revision_text or ""
    return sum(len(m.group(0)) for m in MARKUP_RE.finditer(parent_revision_text))

markup_chars = Feature("parent_revision.markup_chars", process_markup_chars,
                       returns=int, depends_on=[parent_revision.text])

proportion_of_markup_chars = markup_chars / modifiers.max(chars, 1)

def process_numeric_chars(parent_revision_text):
    parent_revision_text = parent_revision_text or ""
    return sum(len(m.group(0)) for m in NUMERIC_RE.finditer(parent_revision_text))

numeric_chars = Feature("parent_revision.numeric_chars", process_numeric_chars,
                        returns=int, depends_on=[parent_revision.text])

proportion_of_numeric_chars = numeric_chars / modifiers.max(chars, 1)

def process_symbolic_chars(parent_revision_text):
    parent_revision_text = parent_revision_text or ""
    return sum(len(m.group(0)) for m in SYMBOLIC_RE.finditer(parent_revision_text))

symbolic_chars = Feature("parent_revision.symbolic_chars",
                         process_symbolic_chars,
                         returns=int, depends_on=[parent_revision.text])

proportion_of_symbolic_chars = symbolic_chars / modifiers.max(chars, 1)

def process_uppercase_chars(parent_revision_text):
    parent_revision_text = parent_revision_text or ""
    return sum(c.lower() != c for c in parent_revision_text)

uppercase_chars = Feature("parent_revision.uppercase_chars",
                          process_uppercase_chars,
                          returns=int, depends_on=[parent_revision.text])

proportion_of_uppercase_chars = uppercase_chars / modifiers.max(chars, 1)


################################## Words #######################################

def process_words(parent_revision_words):
    return len(parent_revision_words)

words = Feature("parent_revision.words", process_words,
                returns=int, depends_on=[parent_revision.words])

def process_badwords(is_badword, parent_revision_words):
    return sum(is_badword(word) for word in parent_revision_words)

badwords = Feature("parent_revision.badwords", process_badwords,
                   returns=int,
                   depends_on=[is_badword, parent_revision.words])

proportion_of_badwords = badwords / modifiers.max(words, 1)

def process_misspellings(is_misspelled, parent_revision_words):
    return sum(is_misspelled(word) for word in parent_revision_words)

misspellings = Feature("parent_revision.misspellings", process_misspellings,
                       returns=int,
                       depends_on=[is_misspelled, parent_revision.words])

proportion_of_misspellings = badwords / modifiers.max(words, 1)

all = [bytes, was_same_user, seconds_since, chars,
       markup_chars, proportion_of_markup_chars,
       numeric_chars, proportion_of_numeric_chars,
       symbolic_chars, proportion_of_symbolic_chars,
       uppercase_chars, proportion_of_uppercase_chars,
       words,
       badwords, proportion_of_badwords,
       misspellings, proportion_of_misspellings]
