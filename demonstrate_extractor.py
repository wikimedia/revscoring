from mw.api import Session

from revscoring.extractors import APIExtractor
from revscoring.features import (added_badwords_ratio, added_misspellings_ratio,
                                 badwords_added, bytes_changed, chars_added,
                                 day_of_week_in_utc, hour_of_day_in_utc,
                                 is_content_namespace, is_custom_comment,
                                 is_mainspace, is_previous_user_same,
                                 is_section_comment,
                                 longest_repeated_char_added,
                                 longest_token_added, misspellings_added,
                                 numeric_chars_added, page_age_in_seconds,
                                 prev_badwords, prev_misspellings, prev_words,
                                 proportion_of_badwords_added,
                                 proportion_of_markup_added,
                                 proportion_of_misspellings_added,
                                 proportion_of_numeric_added,
                                 proportion_of_prev_badwords,
                                 proportion_of_prev_misspellings,
                                 proportion_of_symbolic_added,
                                 proportion_of_uppercase_added,
                                 seconds_since_last_page_edit,
                                 seconds_since_last_user_edit, segments_added,
                                 segments_removed, symbolic_chars_added,
                                 uppercase_chars_added, user_age_in_seconds,
                                 user_is_anon, user_is_bot, words_added,
                                 words_removed)
from revscoring.languages import portuguese

api_extractor = APIExtractor(
    Session("https://pt.wikipedia.org/w/api.php"),
    language=portuguese
)

features = [added_badwords_ratio, added_misspellings_ratio,
            badwords_added, bytes_changed, chars_added,
            day_of_week_in_utc, hour_of_day_in_utc,
            is_content_namespace,
            is_custom_comment, is_mainspace,
            is_previous_user_same, is_section_comment,
            longest_repeated_char_added,
            longest_token_added, misspellings_added,
            numeric_chars_added, page_age_in_seconds,
            prev_badwords, prev_misspellings, prev_words,
            proportion_of_badwords_added,
            proportion_of_markup_added,
            proportion_of_misspellings_added,
            proportion_of_numeric_added,
            proportion_of_prev_badwords,
            proportion_of_prev_misspellings,
            proportion_of_symbolic_added,
            proportion_of_uppercase_added,
            seconds_since_last_page_edit,
            seconds_since_last_user_edit, segments_added,
            segments_removed, symbolic_chars_added,
            uppercase_chars_added, user_age_in_seconds,
            user_is_anon, user_is_bot, words_added,
            words_removed]

print("Extracting features for "  +
      "https://pt.wikipedia.org/w/index.php?diff=4083720")
values = api_extractor.extract(4083720, features)

for feature, value in zip(features, values):
    print("{0}: {1}".format(feature, value))
