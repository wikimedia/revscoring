from collections import OrderedDict

from . import util


class ModelInfo:

    def __init__(self, pairs=[]):
        """
        Constructs a mapping of information about a model.
        :class:`~revscoring.scoring.ModelInfo` objects are usually nested
        within each other to provide a convenient tree structure for
        :func:`~revscoring.scoring.ModelInfo.lookup` and
        :func:`~revscoring.scoring.ModelInfo.format`.
        """
        self._data = OrderedDict(pairs)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, key):
        return key in self._data

    def keys(self):
        return self._data.keys()

    def get(self, key, default=None):
        return self._data.get(key, default)

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __iter__(self):
        return iter(self._data)

    def move_to_end(self, key, last=True):
        return self._data.move_to_end(key, last=last)

    def lookup(self, path=None):
        """
        Looks up a specific information value based on either a string pattern
        or a path.

        For example, the pattern "stats.roc_auc.labels.true" is the same as
        the path ``['stats', 'roc_auc', 'labels', True]``.

        :Parameters:
            path : `str` | `list`
                The location of the information to lookup.
        """
        if isinstance(path, str):
            path = util.parse_pattern(path)
        elif path is None:
            path = []

        d = self
        remaining_path = list(path)  # Make sure we don't overwrite the input
        while len(path) > 0:
            key = path.pop(0)
            try:
                d = d[key]
            except KeyError as e:
                if key in ("true", "false"):
                    d = d[key == 'true']
                else:
                    try:
                        d = d[int(key)]
                    except ValueError:
                        raise e
            if hasattr(d, "lookup"):
                return d.lookup(remaining_path)
            else:
                continue

        return d

    def format(self, paths=None, formatting="str", **kwargs):
        """
        Format a representation of the model information in a useful way.

        :Parameters:
            paths : `iterable` ( `str` | [`str`] )
                A set of paths to use when selecting which information should
                formatted.  Everything beneath a provided path in the tree
                will be formatted.  E.g. `statistics.roc_auc` and `statistics`
                will format redundantly because `roc_auc` is already within
                `statistics`.  Alternatively `statistics.roc_auc` and
                `statistics.pr_auc` will format only those two specific
                bits of information.
            formatting : "json" or "str"
                Which output formatting do you want?  "str" returns something
                nice to show on the command-line.  "json" returns something
                that will pass through :func:`json.dump` without error.
        """
        paths = paths or []
        _paths = [
            util.parse_pattern(path) if isinstance(path, str) else path
            for path in paths]
        if len(_paths) > 0:
            path_tree = util.treeify(_paths)
        else:
            path_tree = OrderedDict((k, {}) for k in self.keys())

        if formatting == "str":
            return self.format_str(path_tree, **kwargs)
        elif formatting == "json":
            return self.format_json(path_tree, **kwargs)
        else:
            raise ValueError("Formatting {0} is not available for {1}."
                             .format(formatting, self.__class__.__name__))

    def format_str(self, path_tree, **kwargs):
        formatted = "Model Information:\n"
        for key in path_tree or self.keys():
            if hasattr(self[key], "format_str"):
                sub_tree = path_tree.get(key, {})
                formatted += util.tab_it_in(
                    self[key].format_str(sub_tree, **kwargs))
            else:
                formatted += util.tab_it_in(" - {0}: {1}"
                                            .format(key, self[key]))

        return formatted

    def format_json(self, path_tree, **kwargs):
        d = OrderedDict()
        for key in path_tree or self.keys():
            if hasattr(self[key], "format_json"):
                sub_tree = path_tree.get(key, {})
                d[key] = self[key].format_json(sub_tree, **kwargs)
            else:
                d[key] = self[key]

        return d
