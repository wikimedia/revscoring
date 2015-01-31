from mw.api import Session

from revscoring.extractors import APIExtractor
from revscoring.features import (bytes_changed, chars_added, day_of_week_in_utc,
                                 hour_of_day_in_utc, is_custom_comment,
                                 user_age_in_seconds, user_is_anon, user_is_bot)

api_extractor = APIExtractor(Session("https://en.wikipedia.org/w/api.php"))

features = [bytes_changed, chars_added, day_of_week_in_utc,
              hour_of_day_in_utc, is_custom_comment, user_age_in_seconds,
              user_is_anon, user_is_bot]

values = api_extractor.extract(
    624577024,
    features
)
for feature, value in zip(features, values):
    print("{0}: {1}".format(feature, value))
