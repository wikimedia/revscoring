import re
from datetime import datetime

from pytz import utc
from revscoring.languages import is_stopword, stem_word

from ..datasources import revision
from .feature import Feature
from .modifiers import max
from .util import (CATEGORY_RE, CITE_RE, IMAGE_RE, INFOBOX_RE,
                   SECTION_COMMENT_RE, SYMBOLIC_RE)


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

################################ Characters ####################################

def process_chars(revision_text):
    return len(revision_text)

chars = Feature("parent_revision.chars", process_chars,
                returns=int, depends_on=[revision.text])

def process_markup_chars(revision_text):
    return sum(1 for _ in MARKUP_RE.finditer(revision_text))

markup_chars = Feature("parent_revision.markup_chars", process_markup_chars,
                       returns=int, depends_on=[revision.text])

proportion_of_markup_chars = markup_chars / max(chars, 1)

def process_numeric_chars(revision_text):
    return sum(1 for _ in NUMERIC_RE.finditer(revision_text))

numeric_chars = Feature("parent_revision.numeric_chars", process_numeric_chars,
                        returns=int, depends_on=[revision.text])

proportion_of_numeric_chars = numeric_chars / max(chars, 1)

def process_symbolic_chars(revision_text):
    return sum(1 for _ in SYMBOLIC_RE.finditer(revision_text))

symbolic_chars = Feature("parent_revision.symbolic_chars",
                         process_symbolic_chars,
                         returns=int, depends_on=[revision.text])

proportion_of_symbolic_chars = symbolic_chars / max(chars, 1)

def process_uppercase_chars(revision_text):
    return sum(c.upper() == c for c in revision_text)

uppercase_chars = Feature("parent_revision.uppercase_chars",
                          process_uppercase_chars,
                          returns=int, depends_on=[revision.text])

proportion_of_uppercase_chars = uppercase_chars / max(chars, 1)


################################ Parse tree ####################################

def level_1_headings_process(headings):
    return sum(h.level==2 for h in headings)

level_1_headings = Feature("level_1_headings", level_1_headings_process,
                           returns=int, depends_on=[revision.headings])
                           
def level_2_headings_process(headings):
   return sum(h.level==2 for h in headings)

level_2_headings = Feature("level_2_headings", level_2_headings_process,
                          returns=int, depends_on=[revision.headings])

def level_3_headings_process(headings):
    return sum(h.level==3 for h in headings)

level_3_headings = Feature("level_3_headings", level_3_headings_process,
                           returns=int, depends_on=[revision.headings])

def level_4_headings_process(headings):
    return sum(h.level==4 for h in headings)

level_4_headings = Feature("level_4_headings", level_4_headings_process,
                           returns=int, depends_on=[revision.headings])

def level_5_headings_process(headings):
    return sum(h.level==5 for h in headings)

level_5_headings = Feature("level_5_headings", level_5_headings_process,
                           returns=int, depends_on=[revision.headings])

def level_6_headings_process(headings):
    return sum(h.level==5 for h in headings)

level_6_headings = Feature("level_6_headings", level_6_headings_process,
                           returns=int, depends_on=[revision.headings])

def process_infonoise(is_stopword, stem_word, content_words):
    non_stopwords = (w for w in content_words if not is_stopword(w))
    non_stopword_stems = (stem_word(w) for w in non_stopwords)
    
    return sum(len(w) for w in non_stopword_stems) / \
           max(sum(len(w) for w in content_words), 1)

infonoise = Feature("infonoise", process_infonoise, returns=float,
                    depends_on=[is_stopword, stem_word, revision.content_words])

def process_internal_links(revision_internal_links):
    return len(revision_internal_links)

internal_links = Feature("internal_links", process_internal_links,
                         returns=int, depends_on=[revision.internal_links])

def process_image_links(revision_internal_links):
    return sum(1 for _ in revision_internal_links
                 if IMAGE_RE.match(str(l.title)))

image_links = Feature("image_links_process", process_image_links,
                      returns=int, depends_on=[revision.internal_links])
                      
def process_category_links(revision_internal_links):
    return sum(1 for _ in revision_internal_links
                 if CATEGORY_RE.match(str(l.title)))

category_links = Feature("category_links", process_category_links,
                         returns=int, depends_on=[revision.internal_links])

def ref_tags_process(revision_tags):
    return sum(1 for tag in revision_tags if tag.tag == "ref")

ref_tags = Feature("ref_tags", ref_tags_process, returns=int,
                   depends_on=[revision.tags])

def process_templates(revision_templates):
    return len(templates_process)

templates = Feature("templates", process_templates,
                    returns=int, depends_on=[revision.templates])

def process_cite_templates(revision_templates):
    return sum(1 for t in templates if CITE_RE.search(str(t.name)))

cite_templates = Feature("cite_templates", process_cite_templates,
                         returns=int, depends_on=[revision.templates])

proportion_of_templated_references = cite_templates / max(ref_tags, 1)

def process_infobox_templates(revision_templates):
    return sum(1 for t in templates if INFOBOX_RE.search(str(t.name)))

infobox_templates = Feature("infobox_templates", process_infobox_templates,
                            returns=int, depends_on=[revision.templates])
