import numpy

from revscoring.scoring.models.util import normalize_json


def test_normalize_json():
    doc = {"foo": {numpy.bool_(True): "value"},
           "what": numpy.bool_(False),
           "this": numpy.PINF}
    normalized_doc = normalize_json(doc)
    assert isinstance(normalized_doc['what'], bool)
    assert isinstance(list(normalized_doc['foo'].keys())[0], bool)
    assert normalized_doc['this'] == "Infinity"
