from mw.api import Session

from revscoring.extractors import APIExtractor
from revscoring.languages import english
from revscoring.scorers import MLScorerModel

api_session = Session("https://en.wikipedia.org/w/api.php")
extractor = APIExtractor(api_session, english)

filename = "models/reverts.halfak_mix.trained.model"
model = MLScorerModel.load(open(filename, 'rb'))

rev_ids = [105, 642215410, 638307884]
feature_values = [extractor.extract(id, model.features) for id in rev_ids]
scores = model.score(feature_values, probabilities=True)
for rev_id, score in zip(rev_ids, scores):
    print("{0}: {1}".format(rev_id, score))
