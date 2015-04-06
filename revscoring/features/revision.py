import re
from datetime import datetime

from pytz import utc
from revscoring.languages import is_stopword, stem_word

from . import modifiers
from ..datasources import revision
from ..languages import is_badword, is_misspelled, is_stopword, stem_word
from .feature import Feature
from .util import (CATEGORY_RE, CITE_RE, IMAGE_RE, INFOBOX_RE, MARKUP_RE,
                   NUMERIC_RE, SECTION_COMMENT_RE, SYMBOLIC_RE)


################################# Time #########################################

def process_day_of_week(revision_metadata):

    dt = datetime.fromtimestamp(revision_metadata.timestamp.unix(), tz=utc)
    return dt.weekday()

day_of_week= Feature("revision.day_of_week", process_day_of_week,
                     returns=int, depends_on=[revision.metadata])

def process_hour_of_day(revision_metadata):

    dt = datetime.fromtimestamp(revision_metadata.timestamp.unix(), tz=utc)
    return dt.hour

hour_of_day = Feature("revision.hour_of_day", process_hour_of_day,
                      returns=int, depends_on=[revision.metadata])

################################ Comment #######################################

def process_has_custom_comment(revision_metadata):

    if revision_metadata.comment is not None:
        trimmed_comment = SECTION_COMMENT_RE.sub("", revision_metadata.comment)
        trimmed_comment = trimmed_comment.strip()

        return len(trimmed_comment) > 1
    else:
        return False

has_custom_comment = Feature("revision.has_custom_comment",
                             process_has_custom_comment,
                             returns=bool, depends_on=[revision.metadata])

def process_has_section_comment(revision_metadata):

    if revision_metadata.comment is not None:
        return SECTION_COMMENT_RE.match(revision_metadata.comment) is not None
    else:
        return False

has_section_comment = \
        Feature("revision.has_section_comment", process_has_section_comment,
                returns=bool, depends_on=[revision.metadata])

################################# Bytes ########################################

def process_bytes(revision_metadata):
    return revision_metadata.bytes or 0

bytes = Feature("revision.bytes", process_bytes,
                returns=int, depends_on=[revision.metadata])

################################ Characters ####################################

def process_chars(revision_text):
    return len(revision_text)

chars = Feature("revision.chars", process_chars,
                returns=int, depends_on=[revision.text])

def process_markup_chars(revision_text):
    return sum(len(m.group(0)) for m in MARKUP_RE.finditer(revision_text))

markup_chars = Feature("revision.markup_chars", process_markup_chars,
                       returns=int, depends_on=[revision.text])

proportion_of_markup_chars = markup_chars / modifiers.max(chars, 1)

def process_numeric_chars(revision_text):
    return sum(len(m.group(0)) for m in NUMERIC_RE.finditer(revision_text))

numeric_chars = Feature("revision.numeric_chars", process_numeric_chars,
                        returns=int, depends_on=[revision.text])

proportion_of_numeric_chars = numeric_chars / modifiers.max(chars, 1)

def process_symbolic_chars(revision_text):
    return sum(len(m.group(0)) for m in SYMBOLIC_RE.finditer(revision_text))

symbolic_chars = Feature("revision.symbolic_chars",
                         process_symbolic_chars,
                         returns=int, depends_on=[revision.text])

proportion_of_symbolic_chars = symbolic_chars / modifiers.max(chars, 1)

def process_uppercase_chars(revision_text):
    return sum(c.lower() != c for c in revision_text)

uppercase_chars = Feature("revision.uppercase_chars",
                          process_uppercase_chars,
                          returns=int, depends_on=[revision.text])

proportion_of_uppercase_chars = uppercase_chars / modifiers.max(chars, 1)

################################## Words #######################################

def process_words(revision_words):
    return len(revision_words)

words = Feature("revision.words", process_words,
                returns=int, depends_on=[revision.words])

def process_badwords(is_badword, revision_words):
    return sum(is_badword(word) for word in revision_words)

badwords = Feature("revision.badwords", process_badwords,
                   returns=int,
                   depends_on=[is_badword, revision.words])

proportion_of_badwords = badwords / modifiers.max(words, 1)

def process_misspellings(is_misspelled, revision_words):
    return sum(is_misspelled(word) for word in revision_words)

misspellings = Feature("revision.misspellings", process_misspellings,
                       returns=int,
                       depends_on=[is_misspelled, revision.words])

proportion_of_misspellings = badwords / modifiers.max(words, 1)


################################ Parse tree ####################################

def process_level_1_headings(headings):
    return sum(h.level==1 for h in headings)

level_1_headings = \
        Feature("revision.level_1_headings", process_level_1_headings,
                returns=int, depends_on=[revision.headings])

def process_level_2_headings(headings):
   return sum(h.level==2 for h in headings)

level_2_headings = \
        Feature("revision.level_2_headings", process_level_2_headings,
                returns=int, depends_on=[revision.headings])

def process_level_3_headings(headings):
    return sum(h.level==3 for h in headings)

level_3_headings = \
        Feature("revision.level_3_headings", process_level_3_headings,
                returns=int, depends_on=[revision.headings])

def process_level_4_headings(headings):
    return sum(h.level==4 for h in headings)

level_4_headings = \
        Feature("revision.level_4_headings", process_level_4_headings,
                returns=int, depends_on=[revision.headings])

def process_level_5_headings(headings):
    return sum(h.level==5 for h in headings)

level_5_headings = \
        Feature("revision.level_5_headings", process_level_5_headings,
                returns=int, depends_on=[revision.headings])

def process_level_6_headings(headings):
    return sum(h.level==5 for h in headings)

level_6_headings = \
        Feature("revision.level_6_headings", process_level_6_headings,
                returns=int, depends_on=[revision.headings])


def process_content_chars(content):
    return len(content)

content_chars = Feature("revision.content_chars", process_content_chars,
                        returns=int, depends_on=[revision.content])

def process_infonoise(is_stopword, stem_word, content_words):
    non_stopwords = (w for w in content_words if not is_stopword(w))
    non_stopword_stems = (stem_word(w) for w in non_stopwords)

    return sum(len(w) for w in non_stopword_stems) / \
           max(sum(len(w) for w in content_words), 1)

infonoise = Feature("revision.infonoise", process_infonoise, returns=float,
                    depends_on=[is_stopword, stem_word, revision.content_words])

def process_internal_links(revision_internal_links):
    return len(revision_internal_links)

internal_links = Feature("revision.internal_links", process_internal_links,
                         returns=int, depends_on=[revision.internal_links])

def process_image_links(revision_internal_links):
    return sum(1 for l in revision_internal_links
                 if IMAGE_RE.match(str(l.title)))

image_links = Feature("revision.image_links", process_image_links,
                      returns=int, depends_on=[revision.internal_links])

def process_category_links(revision_internal_links):
    return sum(1 for l in revision_internal_links
                 if CATEGORY_RE.match(str(l.title)))

category_links = Feature("revision.category_links", process_category_links,
                         returns=int, depends_on=[revision.internal_links])

def ref_tags_process(revision_tags):
    return sum(1 for tag in revision_tags if tag.tag == "ref")

ref_tags = Feature("revision.ref_tags", ref_tags_process, returns=int,
                   depends_on=[revision.tags])

def process_templates(revision_templates):
    return len(revision_templates)

templates = Feature("revision.templates", process_templates,
                    returns=int, depends_on=[revision.templates])

def process_cite_templates(revision_templates):
    return sum(1 for t in revision_templates if CITE_RE.search(str(t.name)))

cite_templates = Feature("revision.cite_templates", process_cite_templates,
                         returns=int, depends_on=[revision.templates])

proportion_of_templated_references = cite_templates / modifiers.max(ref_tags, 1)

def process_infobox_templates(revision_templates):
    return sum(1 for t in revision_templates if INFOBOX_RE.search(str(t.name)))

infobox_templates = Feature("revision.infobox_templates", process_infobox_templates,
                            returns=int, depends_on=[revision.templates])


all = [day_of_week, hour_of_day,
       has_custom_comment, has_section_comment,
       bytes,
       chars, markup_chars, numeric_chars, symbolic_chars, uppercase_chars,
       proportion_of_markup_chars, proportion_of_numeric_chars,
       proportion_of_symbolic_chars, proportion_of_uppercase_chars,
       words, badwords, misspellings,
       level_1_headings, level_2_headings, level_3_headings, level_4_headings,
       level_5_headings, level_6_headings, infonoise, internal_links,
       image_links, category_links, ref_tags, templates, cite_templates,
       infobox_templates]
