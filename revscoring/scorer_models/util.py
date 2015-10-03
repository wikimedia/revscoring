import numpy


def normalize(v, key=False):
    if isinstance(v, numpy.bool_):
        return bool(v)
    elif isinstance(v, numpy.float):
        return float(v)
    elif isinstance(v, tuple):
        if key:
            return str(v)
        else:
            return list(v)
    else:
        return v


def normalize_json(doc):

    if isinstance(doc, dict):
        return {normalize(k, key=True): normalize_json(v)
                for k, v in doc.items()}
    elif isinstance(doc, list):
        return [normalize_json(v) for v in doc]
    else:
        return normalize(doc)
