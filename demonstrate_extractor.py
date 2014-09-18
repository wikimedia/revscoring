from mw.api import Session

from revscores import APIExtractor
from revscores.feature_extractors import (bytes_changed, day_of_week_in_utc,
                                          hour_of_day_in_utc, is_mainspace,
                                          is_previous_user_same,
                                          is_section_comment, num_words_added,
                                          num_words_removed,
                                          page_age_in_seconds, user_is_anon)

api_extractor = APIExtractor(Session("https://en.wikipedia.org/w/api.php"))

features = api_extractor.extract(
    624577024,
    [is_section_comment, user_is_anon, is_mainspace, bytes_changed,
     is_previous_user_same, num_words_added, num_words_removed,
     page_age_in_seconds, day_of_week_in_utc, hour_of_day_in_utc]
)
print(features)
