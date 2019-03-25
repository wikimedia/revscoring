from revscoring import Model
from revscoring.extractors import OfflineExtractor
from revscoring.features import Constant
from revscoring.score_processor import ScoreProcessor


class FakeModel(Model):

    def score(featue_values):
        return not featue_values[0]


def test_score_processor():

    model = FakeModel([Constant(False)])

    sp = ScoreProcessor(model, OfflineExtractor())
    scores = sp.score([1, 2, 3])

    for score in scores:
        assert score
