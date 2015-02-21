from mw.api import Session

from revscoring.extractors import APIExtractor
from revscoring.scorers import MLScorerModel, Scorer

api_session = Session("https://en.wikipedia.org/w/api.php")

filename = "models/reverts.halfak_mix.trained.model"
model = MLScorerModel.load(open(filename, 'rb'))

extractor = APIExtractor(api_session, model.language)
scorer = Scorer({'reverted': model}, extractor)

for rev_id in [105, 642215410, 638307884]:
    score_doc = scorer.score(rev_id)
    print("{0}: {1}".format(rev_id, score_doc))
