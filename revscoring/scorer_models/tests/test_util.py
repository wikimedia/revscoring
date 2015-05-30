from nose.tools import eq_
import numpy
from ..util import normalize_json

def test_normalize_json():
    doc = {"foo": {numpy.bool_(True): "value"}, "what": numpy.bool_(False)}
    normalized_doc = normalize_json(doc)
    eq_(type(normalized_doc['what']), bool)
    eq_(type(list(normalized_doc['foo'].keys())[0]), bool)