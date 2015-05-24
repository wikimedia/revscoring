from collections import namedtuple

from nose.tools import eq_

from ..scorer import Scorer


def test_scorer():
    FakeExtractor = namedtuple("FakeExtractor", ['extract_many', 'language'])
    def fake_extract_many(rev_ids, features, context=None, caches=None):
        d = {'foo': 3, 'bar': 5}
        for rev_id in rev_ids:
            yield None, (d[f] for f in features)
    extractor = FakeExtractor(fake_extract_many, "herpderp")

    FakeModel = namedtuple("FakeModel", ['score', 'features', 'language'])
    multiply = FakeModel(lambda feature_values:feature_values[0] * \
                                               feature_values[1],
                         ["foo", "bar"],
                         "herpderp")
    divide = FakeModel(lambda feature_values:feature_values[0] / \
                                             feature_values[1],
                       ["foo", "bar"],
                       "herpderp")

    scorer = Scorer({"multiply": multiply, "divide": divide}, extractor)

    assert 'foo' in scorer.features()
    assert 'foo' in scorer.dependencies()

    score_doc = scorer.score(1234567890)
    eq_(score_doc['divide'], 3/5)
    eq_(score_doc['multiply'], 3*5)

    score_doc = scorer.score(1234567890, models=['multiply'])
    eq_(score_doc['multiply'], 3*5)
    assert 'divide' not in score_doc
