from collections import OrderedDict

from .. import errors


def parse_pattern(string):
    """
    Parse a statistic lookup pattern
    """
    return list(_parse_pattern(string))


def _parse_pattern(string):
    if len(string) > 0:
        parts = string.split(".")
        buf = []
        for part in parts:
            if buf:
                if part[-1] in ('"', "'") and part[-1] == buf[0][0]:
                    yield (''.join(buf + [part])).strip("'\"")
                    buf = []
                else:
                    buf.append(part + ".")
            elif part[0] in ('"', "'"):
                if part[-1] in ('"', "'") and part[0] == part[-1]:
                    yield part.strip(part[0])
                else:
                    buf.append(part + ".")
            else:
                yield part

        if buf:
            raise ValueError("Parsing error unmatching quotes {0}"
                             .format(''.join(buf)))


_round = round


def round(number, ndigits=0):
    if number is None:
        return None
    else:
        return int(_round((number * (10**ndigits)))) / (10**ndigits)


def tab_it_in(string, tabs=1):
    return "".join("\t" * tabs + "{0}\n".format(line)
                   for line in string.split("\n"))


def tree_assignment(tree, path):
    d = tree
    for k in path:
        if k not in d:
            d[k] = OrderedDict()
        d = d[k]


def treeify(paths):
    tree = {}
    for path in paths:
        tree_assignment(tree, path)
    return tree


def dict_lookup(d, path_tree):
    path_tree = path_tree or {}
    if len(path_tree) == 0:
        return d
    else:
        return OrderedDict(
            (key, dict_lookup(d[key], sub_tree))
            for key, sub_tree in path_tree.items())


def check_label_consistency(actual_labels, expected_labels):
    expected_labels = set(expected_labels)
    unique_labels = set(actual_labels)
    if unique_labels - expected_labels:
        raise errors.ModelConsistencyError(
            "Labels {0} not in list of expected labels {1}"
            .format(unique_labels - expected_labels, expected_labels))
    elif expected_labels - unique_labels:
        raise errors.ModelConsistencyError(
            "Expected labels {0} not represented in the training set"
            .format(expected_labels - unique_labels))
