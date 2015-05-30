import numpy


def normalize(v):
    if isinstance(v, numpy.bool_):
        return bool(v)
    else:
        return v

def normalize_json(doc):
    
    if isinstance(doc, dict):
        return {normalize_json(k):normalize_json(v) for k,v  in doc.items()}
        
    elif isinstance(doc, list):
        return [normalize_json(v) for v in doc]
    
    else:
        
        return normalize(doc)
