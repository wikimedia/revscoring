"""
These meta-datasources operate on :class:`revscoring.Datasource`'s that return
a flat `dict` of key-value pairs (aka a "table") and filter ("select") keys
and/or weight values.

.. autoclass:: revscoring.datasources.meta.selectors.tfidf

.. autoclass:: revscoring.datasources.meta.selectors.filter_keys

"""

from collections import defaultdict
from math import log

from ..datasource import Datasource


class tfidf(Datasource):
    """
    Selects a subset of a frequency table based on term utility and applies
    TF-iDF weighting.

    :Parameters:
        table_datasource : :class:`revscoring.Datasource`
            A datasource that generates a dict of term frequency counts
        max_terms : `int`
            The maximum number of terms that will be selected.  The terms
            with the highest proportional representation in a label class
            are selected.
        weight : `bool`
            Should TF-iDF weighting be applied to output counts?
        boolean : `bool`
            Normalize counts to 0 (not in document) and 1 (in document).  Note
            that negative frequencies will be converted to -1.
        name : `str`
            A name for the datasource.
    """
    def __init__(self, table_datasource, max_terms=None, weight=True,
                 boolean=False, name=None):
        name = self._format_name(
            name, [table_datasource, max_terms, weight, boolean])
        super().__init__(name, self.process,
                         depends_on=[table_datasource])
        self.max_terms = int(max_terms) if max_terms is not None else None
        self.weight = weight
        self.boolean = boolean

    def fit(self, value_labels):
        # Count up document frequencies and label frequencies
        self.document_freq = defaultdict(lambda: 0)
        self.document_n = 0
        label_freq = defaultdict(lambda: defaultdict(lambda: 0))
        label_n = defaultdict(lambda: 0)
        for values, label in value_labels:
            table = values[0]
            for term, freq in table.items():
                if self.boolean:
                    freq = 1 if freq > 0 else -1
                self.document_freq[term] += freq
                self.document_n += 1
                label_freq[label][term] += freq
                label_n[label] += 1

        # Select terms
        if self.max_terms is not None:
            self.document_freq = \
                self._select_terms(label_freq, label_n)

    def _select_terms(self, label_freq, label_n):
        term_utilities = []
        for label, table in label_freq.items():
            for term, label_freq in table.items():
                utility = term_utility(
                    label_freq, label_n[label],
                    self.document_freq[term], self.document_n)
                term_utilities.append((abs(utility), term, label))

        term_utilities.sort(reverse=True)
        new_document_freq = {}
        while len(new_document_freq) < self.max_terms and \
              len(term_utilities) > 0:
            _, term, _ = term_utilities.pop(0)
            new_document_freq[term] = self.document_freq[term]

        return new_document_freq

    def keys(self):
        return self.document_freq.keys()

    def process(self, table):
        new_table = {}
        for term, freq in table.items():
            if self.boolean:
                freq = 1 if freq > 0 else -1
            if term in self.document_freq:
                if self.weight:
                    new_table[term] = \
                        freq * log(self.document_n /
                                   max(self.document_freq[term], 1))
                else:
                    new_table[term] = freq

        return new_table


def term_utility(label_freq, label_n, document_freq, document_n):
    within_label_prop = label_freq / label_n
    extra_label_prop = (document_freq - label_freq) / (document_n - label_n)
    return within_label_prop / max(extra_label_prop, 0.001)


class filter_keys(Datasource):
    """
    Selects a subset of features (key/values) based a set of keys.

    :Parameters:
        table_datasource : :class:`revscoring.Datasource`
            A datasource that generates a table including only the specified
            keys
        keys : `iterable` ( `hashable` )
            The keys to select from the table
        name : `str`
            A name for the datasource.
    """
    def __init__(self, table_datasource, keys, name=None):
        name = self._format_name(
            name, [table_datasource, keys])
        super().__init__(name, self.process,
                         depends_on=[table_datasource])
        self.keys = set(keys)

    def process(self, table):
        new_table = {}
        for key in self.keys:
            if key in table:
                new_table[key] = table[key]

        return new_table
