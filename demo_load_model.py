import mwapi
import requests
from revscoring import ScorerModel
from revscoring.extractors import api

# Get a model from the editquality github
response = requests.get(
    "https://github.com/wiki-ai/editquality/raw/master/models/" +
    "enwiki.damaging.gradient_boosting.model")

scorer_model = ScorerModel.load(f)

extractor = api.Extractor(mwapi.Session(host="https://en.wikipedia.org",
                                        user_agent="revscoring demo"))

feature_values = extractor.extract(123456789, scorer_model.features)

print(scorer_model.score(feature_values))
