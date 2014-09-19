from mw.api import Session

from revscores import APIExtractor
from revscores.feature_extractors import (bytes_changed, chars_added,
                                          day_of_week_in_utc,
                                          hour_of_day_in_utc, is_custom_comment,
                                          is_mainspace, is_previous_user_same,
                                          is_section_comment,
                                          longest_repeated_char_added,
                                          longest_token_added,
                                          num_segments_added,
                                          num_segments_removed, num_words_added,
                                          num_words_removed,
                                          numeric_chars_added,
                                          page_age_in_seconds,
                                          proportion_of_markup_added,
                                          proportion_of_numeric_added,
                                          proportion_of_symbol_added,
                                          proportion_of_uppercase_added,
                                          seconds_since_last_page_edit,
                                          seconds_since_last_user_edit,
                                          uppercase_chars_added,
                                          user_age_in_seconds, user_is_anon,
                                          user_is_bot)

api_extractor = APIExtractor(Session("https://en.wikipedia.org/w/api.php"))

extractors = [bytes_changed, chars_added, day_of_week_in_utc,
              hour_of_day_in_utc, is_custom_comment,is_mainspace,
              is_previous_user_same, is_section_comment,
              longest_repeated_char_added, longest_token_added,
              num_segments_added, num_segments_removed, num_words_added,
              num_words_removed, numeric_chars_added, page_age_in_seconds,
              proportion_of_markup_added, proportion_of_symbol_added,
              proportion_of_numeric_added, proportion_of_uppercase_added,
              seconds_since_last_page_edit, seconds_since_last_user_edit,
              uppercase_chars_added, user_age_in_seconds, user_is_anon,
              user_is_bot]

features = api_extractor.extract(624577024, extractors)

for extractor, feature in zip(extractors, features):
    print("{0}: {1}".format(extractor, feature))
