from . import datasources
from .....datasources.meta import dicts, filters
from ....meta import aggregators

prefix = datasources.prefix

token_delta_sum = aggregators.sum(
    dicts.values(datasources.token_delta),
    name=prefix + ".token_delta_sum"
)
"""
The sum of delta changes in the token frequency table
"""

token_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.token_delta)),
    name=prefix + ".token_delta_increase"
)
"""
The sum of delta increases in the token frequency table
"""

token_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.token_delta)),
    name=prefix + ".token_delta_decrease"
)
"""
The sum of delta decreases in the token frequency table
"""

token_prop_delta_sum = aggregators.sum(
    dicts.values(datasources.token_prop_delta),
    name=prefix + ".token_prop_delta_sum"
)
"""
The sum of proportional delta changes in the token frequency table
"""

token_prop_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.token_prop_delta)),
    name=prefix + ".token_prop_delta_increase"
)
"""
The sum of proportional delta increases in the token frequency table
"""

token_prop_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.token_prop_delta)),
    name=prefix + ".token_prop_delta_decrease"
)
"""
The sum of proportional delta decreases in the token frequency table
"""

# number
number_delta_sum = aggregators.sum(
    dicts.values(datasources.number_delta),
    name=prefix + ".number_delta_sum"
)
"""
The sum of delta changes in the number frequency table
"""

number_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.number_delta)),
    name=prefix + ".number_delta_increase"
)
"""
The sum of delta increases in the number frequency table
"""

number_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.number_delta)),
    name=prefix + ".number_delta_decrease"
)
"""
The sum of delta decreases in the number frequency table
"""

number_prop_delta_sum = aggregators.sum(
    dicts.values(datasources.number_prop_delta),
    name=prefix + ".number_prop_delta_sum"
)
"""
The sum of proportional delta changes in the number frequency table
"""

number_prop_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.number_prop_delta)),
    name=prefix + ".number_prop_delta_increase"
)
"""
The sum of proportional delta increases in the number frequency table
"""

number_prop_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.number_prop_delta)),
    name=prefix + ".number_prop_delta_decrease"
)
"""
The sum of proportional delta decreases in the number frequency table
"""

# whitespace
whitespace_delta_sum = aggregators.sum(
    dicts.values(datasources.whitespace_delta),
    name=prefix + ".whitespace_delta_sum"
)
"""
The sum of delta changes in the whitespace frequency table
"""

whitespace_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.whitespace_delta)),
    name=prefix + ".whitespace_delta_increase"
)
"""
The sum of delta increases in the whitespace frequency table
"""

whitespace_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.whitespace_delta)),
    name=prefix + ".whitespace_delta_decrease"
)
"""
The sum of delta decreases in the whitespace frequency table
"""

whitespace_prop_delta_sum = aggregators.sum(
    dicts.values(datasources.whitespace_prop_delta),
    name=prefix + ".whitespace_prop_delta_sum"
)
"""
The sum of proportional delta changes in the whitespace frequency table
"""

whitespace_prop_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.whitespace_prop_delta)),
    name=prefix + ".whitespace_prop_delta_increase"
)
"""
The sum of proportional delta increases in the whitespace frequency table
"""

whitespace_prop_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.whitespace_prop_delta)),
    name=prefix + ".whitespace_prop_delta_decrease"
)
"""
The sum of proportional delta decreases in the whitespace frequency table
"""

# markup
markup_delta_sum = aggregators.sum(
    dicts.values(datasources.markup_delta),
    name=prefix + ".markup_delta_sum"
)
"""
The sum of delta changes in the markup frequency table
"""

markup_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.markup_delta)),
    name=prefix + ".markup_delta_increase"
)
"""
The sum of delta increases in the markup frequency table
"""

markup_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.markup_delta)),
    name=prefix + ".markup_delta_decrease"
)
"""
The sum of delta decreases in the markup frequency table
"""

markup_prop_delta_sum = aggregators.sum(
    dicts.values(datasources.markup_prop_delta),
    name=prefix + ".markup_prop_delta_sum"
)
"""
The sum of proportional delta changes in the markup frequency table
"""

markup_prop_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.markup_prop_delta)),
    name=prefix + ".markup_prop_delta_increase"
)
"""
The sum of proportional delta increases in the markup frequency table
"""

markup_prop_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.markup_prop_delta)),
    name=prefix + ".markup_prop_delta_decrease"
)
"""
The sum of proportional delta decreases in the markup frequency table
"""

# cjk
cjk_delta_sum = aggregators.sum(
    dicts.values(datasources.cjk_delta),
    name=prefix + ".cjk_delta_sum"
)
"""
The sum of delta changes in the cjk frequency table
"""

cjk_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.cjk_delta)),
    name=prefix + ".cjk_delta_increase"
)
"""
The sum of delta increases in the cjk frequency table
"""

cjk_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.cjk_delta)),
    name=prefix + ".cjk_delta_decrease"
)
"""
The sum of delta decreases in the cjk frequency table
"""

cjk_prop_delta_sum = aggregators.sum(
    dicts.values(datasources.cjk_prop_delta),
    name=prefix + ".cjk_prop_delta_sum"
)
"""
The sum of proportional delta changes in the cjk frequency table
"""

cjk_prop_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.cjk_prop_delta)),
    name=prefix + ".cjk_prop_delta_increase"
)
"""
The sum of proportional delta increases in the cjk frequency table
"""

cjk_prop_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.cjk_prop_delta)),
    name=prefix + ".cjk_prop_delta_decrease"
)
"""
The sum of proportional delta decreases in the cjk frequency table
"""

# entity
entity_delta_sum = aggregators.sum(
    dicts.values(datasources.entity_delta),
    name=prefix + ".entity_delta_sum"
)
"""
The sum of delta changes in the entity frequency table
"""

entity_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.entity_delta)),
    name=prefix + ".entity_delta_increase"
)
"""
The sum of delta increases in the entity frequency table
"""

entity_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.entity_delta)),
    name=prefix + ".entity_delta_decrease"
)
"""
The sum of delta decreases in the entity frequency table
"""

entity_prop_delta_sum = aggregators.sum(
    dicts.values(datasources.entity_prop_delta),
    name=prefix + ".entity_prop_delta_sum"
)
"""
The sum of proportional delta changes in the entity frequency table
"""

entity_prop_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.entity_prop_delta)),
    name=prefix + ".entity_prop_delta_increase"
)
"""
The sum of proportional delta increases in the entity frequency table
"""

entity_prop_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.entity_prop_delta)),
    name=prefix + ".entity_prop_delta_decrease"
)
"""
The sum of proportional delta decreases in the entity frequency table
"""

# url
url_delta_sum = aggregators.sum(
    dicts.values(datasources.url_delta),
    name=prefix + ".url_delta_sum"
)
"""
The sum of delta changes in the url frequency table
"""

url_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.url_delta)),
    name=prefix + ".url_delta_increase"
)
"""
The sum of delta increases in the url frequency table
"""

url_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.url_delta)),
    name=prefix + ".url_delta_decrease"
)
"""
The sum of delta decreases in the url frequency table
"""

url_prop_delta_sum = aggregators.sum(
    dicts.values(datasources.url_prop_delta),
    name=prefix + ".url_prop_delta_sum"
)
"""
The sum of proportional delta changes in the url frequency table
"""

url_prop_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.url_prop_delta)),
    name=prefix + ".url_prop_delta_increase"
)
"""
The sum of proportional delta increases in the url frequency table
"""

url_prop_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.url_prop_delta)),
    name=prefix + ".url_prop_delta_decrease"
)
"""
The sum of proportional delta decreases in the url frequency table
"""

# word
word_delta_sum = aggregators.sum(
    dicts.values(datasources.word_delta),
    name=prefix + ".word_delta_sum"
)
"""
The sum of delta changes in the word frequency table
"""

word_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.word_delta)),
    name=prefix + ".word_delta_increase"
)
"""
The sum of delta increases in the word frequency table
"""

word_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.word_delta)),
    name=prefix + ".word_delta_decrease"
)
"""
The sum of delta decreases in the word frequency table
"""

word_prop_delta_sum = aggregators.sum(
    dicts.values(datasources.word_prop_delta),
    name=prefix + ".word_prop_delta_sum"
)
"""
The sum of proportional delta changes in the word frequency table
"""

word_prop_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.word_prop_delta)),
    name=prefix + ".word_prop_delta_increase"
)
"""
The sum of proportional delta increases in the word frequency table
"""

word_prop_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.word_prop_delta)),
    name=prefix + ".word_prop_delta_decrease"
)
"""
The sum of proportional delta decreases in the word frequency table
"""

# punctuation
punctuation_delta_sum = aggregators.sum(
    dicts.values(datasources.punctuation_delta),
    name=prefix + ".punctuation_delta_sum"
)
"""
The sum of delta changes in the punctuation frequency table
"""

punctuation_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.punctuation_delta)),
    name=prefix + ".punctuation_delta_increase"
)
"""
The sum of delta increases in the punctuation frequency table
"""

punctuation_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.punctuation_delta)),
    name=prefix + ".punctuation_delta_decrease"
)
"""
The sum of delta decreases in the punctuation frequency table
"""

punctuation_prop_delta_sum = aggregators.sum(
    dicts.values(datasources.punctuation_prop_delta),
    name=prefix + ".punctuation_prop_delta_sum"
)
"""
The sum of proportional delta changes in the punctuation frequency table
"""

punctuation_prop_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.punctuation_prop_delta)),
    name=prefix + ".punctuation_prop_delta_increase"
)
"""
The sum of proportional delta increases in the punctuation frequency table
"""

punctuation_prop_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.punctuation_prop_delta)),
    name=prefix + ".punctuation_prop_delta_decrease"
)
"""
The sum of proportional delta decreases in the punctuation frequency table
"""

# break
break_delta_sum = aggregators.sum(
    dicts.values(datasources.break_delta),
    name=prefix + ".break_delta_sum"
)
"""
The sum of delta changes in the break frequency table
"""

break_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.break_delta)),
    name=prefix + ".break_delta_increase"
)
"""
The sum of delta increases in the break frequency table
"""

break_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.break_delta)),
    name=prefix + ".break_delta_decrease"
)
"""
The sum of delta decreases in the break frequency table
"""

break_prop_delta_sum = aggregators.sum(
    dicts.values(datasources.break_prop_delta),
    name=prefix + ".break_prop_delta_sum"
)
"""
The sum of proportional delta changes in the break frequency table
"""

break_prop_delta_increase = aggregators.sum(
    filters.positive(dicts.values(datasources.break_prop_delta)),
    name=prefix + ".break_prop_delta_increase"
)
"""
The sum of proportional delta increases in the break frequency table
"""

break_prop_delta_decrease = aggregators.sum(
    filters.negative(dicts.values(datasources.break_prop_delta)),
    name=prefix + ".break_prop_delta_decrease"
)
"""
The sum of proportional delta decreases in the break frequency table
"""
