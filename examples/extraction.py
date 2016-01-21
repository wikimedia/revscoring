from mwapi import Session
from revscoring.extractors import api
from revscoring.features import temporal, wikitext

session = Session("https://en.wikipedia.org/w/api.php", user_agent="test")
api_extractor = api.Extractor(session)

features = [temporal.revision.day_of_week,
            temporal.revision.hour_of_day,
            wikitext.revision.parent.headings_by_level(2)]

values = api_extractor.extract(624577024, features)
for feature, value in zip(features, values):
    print("\t{0}: {1}".format(feature, repr(value)))
