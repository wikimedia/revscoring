import json

import numpy


def normalize(v):
    if isinstance(v, numpy.bool_):
        return bool(v)
    elif isinstance(v, numpy.ndarray):
        return [normalize(item) for item in v]
    elif v == numpy.NaN:
        return "NaN"
    elif v == numpy.NINF:
        return "-Infinity"
    elif v == numpy.PINF:
        return "Infinity"
    elif isinstance(v, numpy.float):
        return float(v)
    elif isinstance(v, tuple):
        return list(v)
    else:
        return v


def key_normalize(v):
    v = normalize(v)
    if isinstance(v, bool) or isinstance(v, int) or isinstance(v, float) or \
       isinstance(v, str):
        return v
    elif isinstance(v, list) or isinstance(v, dict):
        return json.dumps(v)
    else:
        return str(v)


def normalize_json(doc):
    if isinstance(doc, dict):
        return {key_normalize(k): normalize_json(v)
                for k, v in doc.items()}
    elif isinstance(doc, list) or isinstance(doc, tuple):
        return [normalize_json(v) for v in doc]
    else:
        return normalize(doc)


def format_params(doc):
    if doc is None:
        return None
    else:
        return ", ".join("{0}={1}".format(k, json.dumps(v))
                         for k, v in doc.items())


def tab_it_in(string, tabs=1):
    return "".join("\t" * tabs + "{0}\n".format(line)
                   for line in string.split("\n"))


def balance_weights(labels):
    """
    Generates a mapping of class weights that will re-weight a training set
    in a balanced way such that weight(label) = len(obs) / freq(label in obs).
    """
    counts = {}
    for l in labels:
        counts[l] = counts.get(l, 0) + 1

    return {l: (len(labels) / counts[l]) for l in counts}


def balance_sample_weights(labels):
    """
    Generates a vector of balancing weights for a vector of labels
    """
    weights = balance_weights(labels)
    return [weights[label] for label in labels]
