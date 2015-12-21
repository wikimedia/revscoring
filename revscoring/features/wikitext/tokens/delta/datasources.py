from .....datasources.meta import dicts, frequencies
from ..parent_revision import parent_revision
from ..revision import revision

prefix = "wikitext.tokens.delta"

token_delta = frequencies.delta(
    parent_revision.datasources.token_frequency,
    revision.datasources.token_frequency,
    name=prefix + ".token_delta"
)
"""
A token frequency delta table
"""

token_prop_delta = frequencies.prop_delta(
    parent_revision.datasources.token_frequency,
    token_delta,
    name=prefix + ".token_prop_delta"
)
"""
A token proportional frequency delta table
"""

number_delta = frequencies.delta(
    parent_revision.datasources.number_frequency,
    revision.datasources.number_frequency,
    name=prefix + ".number_delta"
)
"""
A number frequency delta table
"""

number_prop_delta = frequencies.prop_delta(
    parent_revision.datasources.number_frequency,
    number_delta,
    name=prefix + ".number_prop_delta"
)
"""
A number proportional frequency delta table
"""

whitespace_delta = frequencies.delta(
    parent_revision.datasources.whitespace_frequency,
    revision.datasources.whitespace_frequency,
    name=prefix + ".whitespace_delta"
)
"""
A whitespace frequency delta table
"""

whitespace_prop_delta = frequencies.prop_delta(
    parent_revision.datasources.whitespace_frequency,
    whitespace_delta,
    name=prefix + ".whitespace_prop_delta"
)
"""
A whitespace proportional frequency delta table
"""

markup_delta = frequencies.delta(
    parent_revision.datasources.markup_frequency,
    revision.datasources.markup_frequency,
    name=prefix + ".markup_delta"
)
"""
A markup frequency delta table
"""

markup_prop_delta = frequencies.prop_delta(
    parent_revision.datasources.markup_frequency,
    markup_delta,
    name=prefix + ".markup_prop_delta"
)
"""
A markup proportional frequency delta table
"""

cjk_delta = frequencies.delta(
    parent_revision.datasources.cjk_frequency,
    revision.datasources.cjk_frequency,
    name=prefix + ".cjk_delta"
)
"""
A cjk frequency delta table
"""

cjk_prop_delta = frequencies.prop_delta(
    parent_revision.datasources.cjk_frequency,
    cjk_delta,
    name=prefix + ".cjk_prop_delta"
)
"""
A cjk proportional frequency delta table
"""

entity_delta = frequencies.delta(
    parent_revision.datasources.entity_frequency,
    revision.datasources.entity_frequency,
    name=prefix + ".entity_delta"
)
"""
A entity frequency delta table
"""

entity_prop_delta = frequencies.prop_delta(
    parent_revision.datasources.entity_frequency,
    entity_delta,
    name=prefix + ".entity_prop_delta"
)
"""
A entity proportional frequency delta table
"""

url_delta = frequencies.delta(
    parent_revision.datasources.url_frequency,
    revision.datasources.url_frequency,
    name=prefix + ".url_delta"
)
"""
A url frequency delta table
"""

url_prop_delta = frequencies.prop_delta(
    parent_revision.datasources.url_frequency,
    url_delta,
    name=prefix + ".url_prop_delta"
)
"""
A url proportional frequency delta table
"""

word_delta = frequencies.delta(
    parent_revision.datasources.word_frequency,
    revision.datasources.word_frequency,
    name=prefix + ".word_delta"
)
"""
A lower-cased word frequency delta table
"""

word_prop_delta = frequencies.prop_delta(
    parent_revision.datasources.word_frequency,
    word_delta,
    name=prefix + ".word_prop_delta"
)
"""
A lower-cased word proportional frequency delta table
"""

uppercase_word_delta = frequencies.delta(
    parent_revision.datasources.uppercase_word_frequency,
    revision.datasources.uppercase_word_frequency,
    name=prefix + ".uppercase_word_delta"
)
"""
A uppercase word frequency delta table
"""

uppercase_word_prop_delta = frequencies.prop_delta(
    parent_revision.datasources.uppercase_word_frequency,
    uppercase_word_delta,
    name=prefix + ".uppercase_word_prop_delta"
)
"""
A uppercase word proportional frequency delta table
"""

punctuation_delta = frequencies.delta(
    parent_revision.datasources.punctuation_frequency,
    revision.datasources.punctuation_frequency,
    name=prefix + ".punctuation_delta"
)
"""
A punctuation frequency delta table
"""

punctuation_prop_delta = frequencies.prop_delta(
    parent_revision.datasources.punctuation_frequency,
    punctuation_delta,
    name=prefix + ".punctuation_prop_delta"
)
"""
A punctuation proportional frequency delta table
"""

break_delta = frequencies.delta(
    parent_revision.datasources.break_frequency,
    revision.datasources.break_frequency,
    name=prefix + ".break_delta"
)
"""
A break frequency delta table
"""

break_prop_delta = frequencies.prop_delta(
    parent_revision.datasources.break_frequency,
    break_delta,
    name=prefix + ".break_prop_delta"
)
"""
A break proportional frequency delta table
"""
