import logging

from tabulate import tabulate

from ... import util
from ...model_info import ModelInfo

logger = logging.getLogger(__name__)


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

        self['labels'] = {label: lstats[field]
                          for label, lstats in stats.items()}

    def format_str(self, path_tree, ndigits=3, **kwargs):
        if len(path_tree) > 0:
            logger.warn("Ignoring path_tree at {0!r}".format(path_tree))
        formatted = "{0} (micro={1}, macro={2}):\n" \
            .format(self.field,
                    util.round(self['micro'], ndigits=ndigits),
                    util.round(self['macro'], ndigits=ndigits))
        table_str = tabulate(
            [[util.round(stat, ndigits)
              for l, stat in self['labels'].items()]],
            headers=self['labels'].keys())
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
