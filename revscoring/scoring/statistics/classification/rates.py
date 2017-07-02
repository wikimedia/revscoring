import logging
from collections import OrderedDict

from tabulate import tabulate

from ... import util
from ...model_info import ModelInfo

logger = logging.getLogger(__name__)


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
        table_data = [
            [group] + [util.round(self[group].get(label), ndigits)
                       for label in self['sample']]
            for group in self]

        table_str = tabulate(
            table_data, headers=[''] + [repr(l) for l in self['sample']])
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
