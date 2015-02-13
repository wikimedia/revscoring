from mw.api import Session

from revscoring.extractors import APIExtractor
from revscoring.scorers import MLScorer, MLScorerModel

api_session = Session("https://en.wikipedia.org/w/api.php")

filename = "models/reverts.halfak_mix.trained.model"
model = MLScorerModel.load(open(filename, 'rb'))

extractor = APIExtractor(api_session, model.language)
scorer = MLScorer(extractor, model)

rev_ids = [105, 642215410, 638307884]
scores = scorer.score(rev_ids)
for rev_id, score in zip(rev_ids, scores):
    print("{0}: {1}".format(rev_id, score))
