from mw.api import Session

from revscoring.extractors import APIExtractor
from revscoring.languages import english
from revscoring.scorers import MLScorerModel

api_session = Session("https://en.wikipedia.org/w/api.php")
extractor = APIExtractor(api_session, english)

filename = "models/reverts.halfak_mix.trained.model"
model = MLScorerModel.load(open(filename, 'rb'))

[s for s in model.score([extractor.extract(642215410, model.features)])]
