from .. import Model
from ..extractors import OfflineExtractor
from ..features import Constant
from ..score_processor import ScoreProcessor


class FakeModel(Model):

    def score(featue_values):
        return not featue_values[0]


def test_score_processor():

    model = FakeModel([Constant(False)])

    sp = ScoreProcessor(model, OfflineExtractor())
    scores = sp.score([1, 2, 3])

    for score in scores:
        assert score
