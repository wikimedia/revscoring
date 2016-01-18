import mwapi
from revscoring import ScorerModel
from revscoring.extractors import api

with open("models/enwiki.damaging.linear_svc.model") as f:
    model = ScorerModel.load(f)

extractor = api.Extractor(mwapi.Session(host="https://en.wikipedia.org",
                                         user_agent="revscoring demo"))
values = extractor.extract(123456789, model.features)
print(model.score(values))
