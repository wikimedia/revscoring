from mw.api import Session

from revscores import APIExtractor
from revscores.feature_extractors import (bytes_changed, chars_added,
                                          day_of_week_in_utc,
                                          hour_of_day_in_utc, is_mainspace,
                                          is_previous_user_same,
                                          is_section_comment,
                                          longest_character_repetition_added,
                                          longest_token_added,
                                          num_segments_added,
                                          num_segments_removed, num_words_added,
                                          num_words_removed,
                                          numeric_chars_added,
                                          page_age_in_seconds,
                                          proportion_of_numeric_added,
                                          proportion_of_uppercase_added,
                                          seconds_since_last_page_edit,
                                          uppercase_chars_added, user_is_anon)

api_extractor = APIExtractor(Session("https://en.wikipedia.org/w/api.php"))

features = api_extractor.extract(
    624577024,
    [is_section_comment, user_is_anon, is_mainspace, bytes_changed,
     is_previous_user_same, num_words_added, num_words_removed,
     page_age_in_seconds, day_of_week_in_utc, hour_of_day_in_utc,
     longest_character_repetition_added, longest_token_added,
     num_segments_added, num_segments_removed, chars_added,
     uppercase_chars_added, proportion_of_uppercase_added,
     numeric_chars_added, proportion_of_numeric_added,
     seconds_since_last_page_edit]
)
print(features)
