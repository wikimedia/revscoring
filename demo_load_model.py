import mwapi
from revscoring import ScorerModel
from revscoring.extractors import APIExtractor

with open("models/enwiki.damaging.linear_svc.model") as f:
    scorer_model = ScorerModel.load(f)

extractor = APIExtractor(mwapi.Session(host="https://en.wikipedia.org",
                                       user_agent="revscoring demo"))

feature_values = extractor.extract(123456789, scorer_model.features)

print(scorer_model.score(feature_values))
