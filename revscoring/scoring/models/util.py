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
