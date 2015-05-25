import sys

from mw.api import Session

sys.path.insert(0, ".")
from revscoring.extractors import APIExtractor
from revscoring.features import (diff, page, parent_revision,
                                 previous_user_revision, revision, user)
from revscoring.languages import portuguese

api_extractor = APIExtractor(
    Session("https://pt.wikipedia.org/w/api.php"),
    language=portuguese
)

features = [diff.added_badwords_ratio, diff.added_markup_chars_ratio,
            diff.added_misspellings_ratio, diff.added_number_chars_ratio,
            diff.added_symbolic_chars_ratio, diff.added_uppercase_chars_ratio,
            diff.badwords_added, diff.badwords_removed, diff.chars_added,
            diff.chars_removed, diff.longest_repeated_char_added,
            diff.longest_token_added, diff.markup_chars_added,
            diff.markup_chars_removed, diff.misspellings_added,
            diff.misspellings_removed, diff.numeric_chars_added,
            diff.numeric_chars_removed,
            diff.proportion_of_badwords_added,
            diff.proportion_of_badwords_removed,
            diff.proportion_of_chars_added,
            diff.proportion_of_chars_removed,
            diff.proportion_of_markup_chars_added,
            diff.proportion_of_misspellings_added,
            diff.proportion_of_misspellings_removed,
            diff.proportion_of_numeric_chars_added,
            diff.proportion_of_symbolic_chars_added,
            diff.proportion_of_uppercase_chars_added,
            diff.removed_badwords_ratio,
            diff.removed_misspellings_ratio,
            diff.segments_added, diff.segments_removed,
            diff.symbolic_chars_added, diff.symbolic_chars_removed,
            diff.uppercase_chars_added, diff.uppercase_chars_removed,
            diff.words_added, diff.words_removed,
            diff.bytes_changed, diff.bytes_changed_ratio,
            page.age, page.is_mainspace, page.is_content_namespace,
            parent_revision.badwords, parent_revision.bytes,
            parent_revision.chars, parent_revision.markup_chars,
            parent_revision.misspellings,
            parent_revision.numeric_chars,
            parent_revision.proportion_of_badwords,
            parent_revision.proportion_of_markup_chars,
            parent_revision.proportion_of_misspellings,
            parent_revision.proportion_of_numeric_chars,
            parent_revision.proportion_of_symbolic_chars,
            parent_revision.proportion_of_uppercase_chars,
            parent_revision.revision_bytes,
            parent_revision.seconds_since, parent_revision.symbolic_chars,
            parent_revision.uppercase_chars, parent_revision.was_same_user,
            parent_revision.words,
            previous_user_revision.seconds_since,
            revision.badwords, revision.bytes, revision.category_links,
            revision.chars, revision.cite_templates,
            revision.day_of_week, revision.has_custom_comment,
            revision.has_section_comment, revision.hour_of_day,
            revision.image_links, revision.infobox_templates,
            revision.content_chars,
            revision.infonoise, revision.internal_links,
            revision.level_1_headings,
            revision.level_2_headings,
            revision.level_3_headings,
            revision.level_4_headings,
            revision.level_5_headings,
            revision.level_6_headings,
            revision.markup_chars, revision.misspellings,
            revision.numeric_chars, revision.proportion_of_badwords,
            revision.proportion_of_markup_chars,
            revision.proportion_of_misspellings,
            revision.proportion_of_numeric_chars,
            revision.proportion_of_symbolic_chars,
            revision.proportion_of_templated_references,
            revision.proportion_of_uppercase_chars,
            revision.ref_tags, revision.symbolic_chars,
            revision.templates, revision.uppercase_chars, revision.words,
            user.age, user.is_anon, user.is_bot]

print("Extracting {0} features for ".format(len(features))  +
      "https://pt.wikipedia.org/w/index.php?diff=4083720")
values = api_extractor.extract(4083720, features)

for feature, value in zip(features, values):
    print("{0}: {1}".format(feature, value))
    sys.stdout.flush()
