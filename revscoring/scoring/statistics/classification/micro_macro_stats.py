import logging

from collections import OrderedDict
from tabulate import tabulate

from ... import util
from ...model_info import ModelInfo

logger = logging.getLogger(__name__)

MAX_COLUMNS_WIDTH_CHARS = 80


class MicroMacroStats(ModelInfo):

    def __init__(self, stats, field):
        """
        Constructs a micro-average and macro-average for a specific statistic
        based on the name.  Works like a dictionary with fields

         * micro : the micro-average
         * macro : the macro-average
         * labels : a mapping of labels to their individual statistics

        :Parameters:
        """  # noqa
        super().__init__()
        self.field = field
        try:
            self['micro'] = (
                sum(lstats[field] * lstats.trues
                    for lstats in stats.values()) /
                sum(lstats.trues for lstats in stats.values()))
        except Exception as e:
            logger.warn("Could not generate micro-average of {0}: {1}"
                        .format(field, str(e)))
            self['micro'] = None

        try:
            self['macro'] = (
                sum(lstats[field] for lstats in stats.values()) /
                len(stats))
        except Exception as e:
            logger.warn("Could not generate macro-average of {0}: {1}"
                        .format(field, str(e)))
            self['macro'] = None

        self['labels'] = OrderedDict()
        for label, lstats in stats.items():
            self['labels'][label] = lstats[field]

    def format_str(self, path_tree, ndigits=3, **kwargs):
        if len(path_tree) > 0:
            logger.warn("Ignoring path_tree at {0!r}".format(path_tree))
        formatted = "{0} (micro={1}, macro={2}):\n" \
            .format(self.field,
                    util.round(self['micro'], ndigits=ndigits),
                    util.round(self['macro'], ndigits=ndigits))

        table_str = self.format_label_table(ndigits)

        formatted += util.tab_it_in(table_str)
        return formatted

    def format_json(self, path_tree, ndigits=3):
        if len(path_tree) > 0:
            logger.warn("Ignoring path_tree at {0!r}".format(path_tree))
        return {
            'micro': util.round(self['micro'], ndigits),
            'macro': util.round(self['macro'], ndigits),
            'labels': {l: util.round(self['labels'][l], ndigits)
                       for l in self['labels']}
        }

    def format_label_table(self, ndigits):
        column_header_width = sum(max(len(str(l)) + 2, ndigits + 4)
                                  for l in self['labels'])
        if column_header_width < MAX_COLUMNS_WIDTH_CHARS:
            return self.format_column_major_table(ndigits)
        else:
            return self.format_row_major_table(ndigits)

    def format_row_major_table(self, ndigits):
        return tabulate(
            [[l, util.round(stat, ndigits)]
             for l, stat in self['labels'].items()])

    def format_column_major_table(self, ndigits):
        return tabulate(
            [[util.round(stat, ndigits)
              for l, stat in self['labels'].items()]],
            headers=self['labels'].keys())
