from mw.api import Session

from revscores import APIExtractor
from revscores.feature_extractors import (bytes_changed, chars_added,
                                          day_of_week_in_utc,
                                          hour_of_day_in_utc, is_custom_comment,
                                          user_age_in_seconds, user_is_anon,
                                          user_is_bot)

api_extractor = APIExtractor(Session("https://en.wikipedia.org/w/api.php"))

extractors = [bytes_changed, chars_added, day_of_week_in_utc,
              hour_of_day_in_utc, is_custom_comment, user_age_in_seconds,
              user_is_anon, user_is_bot]

features = api_extractor.extract(
    624577024,
    extractors
)
for extractor, feature in zip(extractors, features):
    print("{0}: {1}".format(extractor, feature))
