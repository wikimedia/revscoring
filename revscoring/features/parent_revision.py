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
"""
Represents size of parent revision's content in bytes.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.bytes]))
        [23731]
"""
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
"""
Represents whether the last edit was made by this user or not.

:Returns:
    bool

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.was_same_user]))
        [False]
"""

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
"""
Represents time between this edit and the last edit in seconds.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.seconds_since]))
        [822837]
"""
################################# Characters #################################

def process_chars(parent_revision_text):
    return len(parent_revision_text or "")

chars = Feature("parent_revision.chars", process_chars,
                returns=int, depends_on=[parent_revision.text])
"""
Represents number of characters in parent revision's content.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.chars]))
        [23719]
"""

def process_markup_chars(parent_revision_text):
    parent_revision_text = parent_revision_text or ""
    return sum(len(m.group(0)) for m in MARKUP_RE.finditer(parent_revision_text))

markup_chars = Feature("parent_revision.markup_chars", process_markup_chars,
                       returns=int, depends_on=[parent_revision.text])
"""
Represents number of markup characters in parent revision's content.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.markup_chars]))
        [700]
"""
proportion_of_markup_chars = markup_chars / modifiers.max(chars, 1)
"""
Represents ratio of markup characters compared to all characters in parent
revision's content.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.proportion_of_markup_chars]))
        [0.02951220540494962]
"""
def process_numeric_chars(parent_revision_text):
    parent_revision_text = parent_revision_text or ""
    return sum(len(m.group(0)) for m in NUMERIC_RE.finditer(parent_revision_text))

numeric_chars = Feature("parent_revision.numeric_chars", process_numeric_chars,
                        returns=int, depends_on=[parent_revision.text])
"""
Represents number of numeric characters in parent revision's content.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.numeric_chars]))
        [203]
"""

proportion_of_numeric_chars = numeric_chars / modifiers.max(chars, 1)
"""
Represents ratio of numeric characters compared to all characters in parent
revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.proportion_of_numeric_chars]))
        [0.008558539567435389]
"""
def process_symbolic_chars(parent_revision_text):
    parent_revision_text = parent_revision_text or ""
    return sum(len(m.group(0)) for m in SYMBOLIC_RE.finditer(parent_revision_text))

symbolic_chars = Feature("parent_revision.symbolic_chars",
                         process_symbolic_chars,
                         returns=int, depends_on=[parent_revision.text])
"""
Represents number of symbolic characters in parent revision's content.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.symbolic_chars]))
        [2539]
"""
proportion_of_symbolic_chars = symbolic_chars / modifiers.max(chars, 1)
"""
Represents ratio of symbolic characters compared to all characters in parent
revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.proportion_of_symbolic_chars]))
        [0.10704498503309583]
"""

def process_uppercase_chars(parent_revision_text):
    parent_revision_text = parent_revision_text or ""
    return sum(c.lower() != c for c in parent_revision_text)

uppercase_chars = Feature("parent_revision.uppercase_chars",
                          process_uppercase_chars,
                          returns=int, depends_on=[parent_revision.text])
"""
Represents number of uppercase characters in parent revision's content.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.uppercase_chars]))
        [733]
"""

proportion_of_uppercase_chars = uppercase_chars / modifiers.max(chars, 1)
"""
Represents ratio of uppercase characters compared to all characters in parent
revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.proportion_of_uppercase_chars]))
        [0.030903495088325815]
"""

################################## Words #######################################

def process_words(parent_revision_words):
    return len(parent_revision_words)

words = Feature("parent_revision.words", process_words,
                returns=int, depends_on=[parent_revision.words])
"""
Represents number of words in parent revision's content.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.words]))
        [3714]
"""

def process_badwords(is_badword, parent_revision_words):
    return sum(is_badword(word) for word in parent_revision_words)

badwords = Feature("parent_revision.badwords", process_badwords,
                   returns=int,
                   depends_on=[is_badword, parent_revision.words])
"""
Represents number of bad words in parent revision's content.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.badwords]))
        [136]
"""

proportion_of_badwords = badwords / modifiers.max(words, 1)
"""
Represents ratio of bad words compared to all words in parent revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [parent_revision.proportion_of_badwords]))
        [0.0366182014001077]
"""
def process_misspellings(is_misspelled, parent_revision_words):
    return sum(is_misspelled(word) for word in parent_revision_words)

misspellings = Feature("parent_revision.misspellings", process_misspellings,
                       returns=int,
                       depends_on=[is_misspelled, parent_revision.words])
"""
Represents number of misspelled words in parent revision's content.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(646076603, [parent_revision.misspellings]))
        [4524]
"""
proportion_of_misspellings = misspellings / modifiers.max(words, 1)
"""
Represents ratio of misspelled words compared to all words in parent revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(646076603, [parent_revision.proportion_of_misspellings]))
        [0.0006516587677725119]
"""

all = [bytes, was_same_user, seconds_since, chars,
       markup_chars, proportion_of_markup_chars,
       numeric_chars, proportion_of_numeric_chars,
       symbolic_chars, proportion_of_symbolic_chars,
       uppercase_chars, proportion_of_uppercase_chars,
       words,
       badwords, proportion_of_badwords,
       misspellings, proportion_of_misspellings]
