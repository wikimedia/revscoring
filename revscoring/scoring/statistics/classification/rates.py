import logging
from collections import OrderedDict

from tabulate import tabulate

from ... import util
from ...model_info import ModelInfo

logger = logging.getLogger(__name__)

MAX_COLUMNS_WIDTH_CHARS = 80


class Rates(ModelInfo):

    def __init__(self, counts, population_rates=None):
        super().__init__()
        self['sample'] = OrderedDict(
            (label, lcount / counts['n'])
            for label, lcount in counts['labels'].items())
        if population_rates:
            self['population'] = OrderedDict(
                (label, population_rates[label]) for label in counts['labels'])

    def format_str(self, path_tree, ndigits=3, **kwargs):
        if len(path_tree) > 0:
            logger.warn("Ignoring path_tree={0!r} while formatting rates."
                        .format(path_tree))

        formatted = "rates:\n"
        table_str = self.format_table(ndigits)
        formatted += util.tab_it_in(table_str)
        return formatted

    def format_json(self, path_tree, ndigits=3, **kwargs):
        doc = OrderedDict()
        for key in path_tree or self.keys():
            sub_tree = path_tree.get(key, {})
            if len(sub_tree) > 0:
                logger.warn("Ignoring path_tree={0!r} while formatting rates."
                            .format(sub_tree))
            group = self[key]
            doc[key] = {l: util.round(group[l], ndigits) for l in group}
        return doc

    def format_table(self, ndigits):
        column_header_width = sum(max(len(str(l)) + 2, ndigits + 4)
                                  for l in self['sample'])
        if column_header_width < MAX_COLUMNS_WIDTH_CHARS:
            return self.format_column_major_table(ndigits)
        else:
            return self.format_row_major_table(ndigits)

    def format_column_major_table(self, ndigits):
        return tabulate(
            [[group] + [util.round(self[group].get(label), ndigits)
                           for label in self['sample']]
             for group in self],
            headers=[''] + [repr(l) for l in self['sample']])

    def format_row_major_table(self, ndigits):
        return tabulate(
            [([label] +
              [util.round(self[group][label], ndigits) for group in self])
             for label in self['sample']],
            headers=[''] + list(self.keys()))
