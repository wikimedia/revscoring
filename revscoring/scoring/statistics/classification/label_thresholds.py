import logging
from collections import OrderedDict

from ... import util
from ...model_info import ModelInfo

logger = logging.getLogger(__name__)


class LabelThresholds(ModelInfo):

    def lookup(self, path):
        if len(path) > 0:
            key = path[0]
            if len(path[1:]) > 0:
                logger.warn("Ignoring path at {0!r}".format(path[1:]))
            return self[key]
        else:
            return self

    def format_str(self, path_tree, **kwargs):
        formatted = "thresholds:\n"
        for label in path_tree.keys() or self.keys():
            sub_tree = path_tree.get(label, {})
            formatted += util.tab_it_in(repr(label))
            table_str = self[label].format_str(sub_tree, **kwargs)
            formatted += util.tab_it_in(table_str, 2)
            formatted += "\n"
        return formatted

    def format_json(self, path_tree, **kwargs):
        doc = OrderedDict
        for label in path_tree.keys() or self.keys():
            sub_tree = path_tree.get(label, {})
            doc[label] = self[label].format_json(sub_tree, **kwargs)
        return doc
