from mw.api import Session
from revscoring.extractors import APIExtractor
from revscoring.features import diff, parent_revision, revision, user

api_extractor = APIExtractor(Session("https://en.wikipedia.org/w/api.php"))

features = [revision.day_of_week,
            revision.hour_of_day,
            revision.has_custom_comment,
            diff.bytes_changed,
            diff.chars_added,
            user.age,
            user.is_anon,
            user.is_bot]

values = api_extractor.extract(
    624577024,
    features
)
for feature, value in zip(features, values):
    print("{0}: {1}".format(feature, value))
