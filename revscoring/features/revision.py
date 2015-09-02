from datetime import datetime

from pytz import utc

from . import modifiers
from ..datasources import revision
from .feature import Feature
# TODO: Many of these are enwiki specific -- they shouldn't be.
from .util import (CATEGORY_RE, CITE_RE, IMAGE_RE, INFOBOX_RE, MARKUP_RE,
                   NUMERIC_RE, SECTION_COMMENT_RE, SYMBOLIC_RE)


# ############################### Time ########################################

def process_day_of_week(revision_metadata):

    dt = datetime.fromtimestamp(revision_metadata.timestamp.unix(), tz=utc)
    return dt.weekday()

day_of_week = Feature("revision.day_of_week", process_day_of_week,
                      returns=int, depends_on=[revision.metadata])
"""
Represents day of week when the edit was made in UTC.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.day_of_week]))
        [6]
"""


def process_hour_of_day(revision_metadata):

    dt = datetime.fromtimestamp(revision_metadata.timestamp.unix(), tz=utc)
    return dt.hour

hour_of_day = Feature("revision.hour_of_day", process_hour_of_day,
                      returns=int, depends_on=[revision.metadata])
"""
Represents hour of day when the edit was made in UTC.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.hour_of_day]))
        [21]
"""


# ############################### Comment #####################################
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
"""
Represents whether the edit has custom edit summary.

:Returns:
    bool

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.has_custom_comment]))
        [False]
"""


def process_has_section_comment(revision_metadata):

    if revision_metadata.comment is not None:
        return SECTION_COMMENT_RE.match(revision_metadata.comment) is not None
    else:
        return False

has_section_comment = \
    Feature("revision.has_section_comment", process_has_section_comment,
            returns=bool, depends_on=[revision.metadata])
"""
Represents whether the edit has section edit summary.

Section edit summaries are like ``"/* <section title> */"`` which mediawiki
automatically creates them when a user edit a section.

:Returns:
    bool

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.has_section_comment]))
        [True]
"""


# ################################ Bytes ######################################
def process_bytes(revision_metadata):
    return revision_metadata.bytes or 0

bytes = Feature("revision.bytes", process_bytes,
                returns=int, depends_on=[revision.metadata])
"""
Represents size of the revision's content in bytes. It uses UTF-8 encoding.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.bytes]))
        [24028]
"""


# ############################### Characters ##################################
def process_chars(revision_text):
    return len(revision_text)

chars = Feature("revision.chars", process_chars,
                returns=int, depends_on=[revision.text])
"""
Represents number of characters in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.chars]))
        [24016]
"""


def process_markup_chars(revision_text):
    return sum(len(m.group(0)) for m in MARKUP_RE.finditer(revision_text))

markup_chars = Feature("revision.markup_chars", process_markup_chars,
                       returns=int, depends_on=[revision.text])
"""
Represents number of markup characters in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.markup_chars]))
        [704]
"""

proportion_of_markup_chars = markup_chars / modifiers.max(chars, 1)
"""
Represents ratio of markup characters compared to all characters in revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130,
        ...      [revision.proportion_of_markup_chars]))
        [0.029313790806129246]
"""


def process_numeric_chars(revision_text):
    return sum(len(m.group(0)) for m in NUMERIC_RE.finditer(revision_text))

numeric_chars = Feature("revision.numeric_chars", process_numeric_chars,
                        returns=int, depends_on=[revision.text])
"""
Represents number of numeric characters in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.numeric_chars]))
        [203]
"""

proportion_of_numeric_chars = numeric_chars / modifiers.max(chars, 1)
"""
Represents ratio of numeric characters compared to all characters in revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130,
        ...      [revision.proportion_of_numeric_chars]))
        [0.008452698201199201]
"""


def process_symbolic_chars(revision_text):
    return sum(len(m.group(0)) for m in SYMBOLIC_RE.finditer(revision_text))

symbolic_chars = Feature("revision.symbolic_chars",
                         process_symbolic_chars,
                         returns=int, depends_on=[revision.text])
"""
Represents number of symbolic characters in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.symbolic_chars]))
        [2559]
"""

proportion_of_symbolic_chars = symbolic_chars / modifiers.max(chars, 1)
"""
Represents ratio of symbolic characters compared to all characters in revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130,
        ...      [revision.proportion_of_symbolic_chars]))
        [0.10655396402398401]
"""


def process_uppercase_chars(revision_text):
    return sum(c.lower() != c for c in revision_text)

uppercase_chars = Feature("revision.uppercase_chars",
                          process_uppercase_chars,
                          returns=int, depends_on=[revision.text])
"""
Represents number of uppercase characters in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.uppercase_chars]))
        [742]
"""

proportion_of_uppercase_chars = uppercase_chars / modifiers.max(chars, 1)
"""
Represents ratio of uppercase characters compared to all characters in
revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130,
        ...      [revision.proportion_of_uppercase_chars]))
        [0.030896069287141906]
"""


# ############################## Parse tree ###################################
def process_level_1_headings(headings):
    return sum(h.level == 1 for h in headings)

level_1_headings = \
    Feature("revision.level_1_headings", process_level_1_headings,
            returns=int, depends_on=[revision.headings])
"""
Represents number of first level headings in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.level_1_headings]))
        [0]
"""


def process_level_2_headings(headings):
    return sum(h.level == 2 for h in headings)

level_2_headings = \
    Feature("revision.level_2_headings", process_level_2_headings,
            returns=int, depends_on=[revision.headings])
"""
Represents number of second level headings in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.level_2_headings]))
        [6]
"""


def process_level_3_headings(headings):
    return sum(h.level == 3 for h in headings)

level_3_headings = \
    Feature("revision.level_3_headings", process_level_3_headings,
            returns=int, depends_on=[revision.headings])
"""
Represents number of third level headings in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.level_3_headings]))
        [13]
"""


def process_level_4_headings(headings):
    return sum(h.level == 4 for h in headings)

level_4_headings = \
    Feature("revision.level_4_headings", process_level_4_headings,
            returns=int, depends_on=[revision.headings])
"""
Represents number of forth level headings in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.level_4_headings]))
        [4]
"""


def process_level_5_headings(headings):
    return sum(h.level == 5 for h in headings)

level_5_headings = \
    Feature("revision.level_5_headings", process_level_5_headings,
            returns=int, depends_on=[revision.headings])
"""
Represents number of fifth level headings in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.level_5_headings]))
        [0]
"""


def process_level_6_headings(headings):
    return sum(h.level == 5 for h in headings)

level_6_headings = \
    Feature("revision.level_6_headings", process_level_6_headings,
            returns=int, depends_on=[revision.headings])
"""
Represents number of sixth level headings in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.level_6_headings]))
        [0]
"""


def process_content_chars(content):
    return len(content)

content_chars = Feature("revision.content_chars", process_content_chars,
                        returns=int, depends_on=[revision.content])
"""
Represents number of content characters in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.content_chars]))
        [19363]
"""


def process_internal_links(revision_internal_links):
    return len(revision_internal_links)

internal_links = Feature("revision.internal_links", process_internal_links,
                         returns=int, depends_on=[revision.internal_links])
"""
Represents number of internal links in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [revision.internal_links]))
        [146]
"""


def process_image_links(revision_internal_links):
    return sum(1 for l in revision_internal_links
               if IMAGE_RE.match(str(l.title)))

image_links = Feature("revision.image_links", process_image_links,
                      returns=int, depends_on=[revision.internal_links])
"""
Represents number of image links in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(661258898, [revision.image_links]))
        [13]
"""


def process_category_links(revision_internal_links):
    return sum(1 for l in revision_internal_links
               if CATEGORY_RE.match(str(l.title)))

category_links = Feature("revision.category_links", process_category_links,
                         returns=int, depends_on=[revision.internal_links])
"""
Represents number of category links in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(661258898, [revision.category_links]))
        [50]
"""


def ref_tags_process(revision_tags):
    return sum(1 for tag in revision_tags if tag.tag == "ref")

ref_tags = Feature("revision.ref_tags", ref_tags_process, returns=int,
                   depends_on=[revision.tags])
"""
Represents number of reference tags in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(661258898, [revision.ref_tags]))
        [228]
"""


def process_templates(revision_templates):
    return len(revision_templates)

templates = Feature("revision.templates", process_templates,
                    returns=int, depends_on=[revision.templates])
"""
Represents number of templates in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(661258898, [revision.templates]))
        [287]
"""


def process_cite_templates(revision_templates):
    return sum(1 for t in revision_templates if CITE_RE.search(str(t.name)))

cite_templates = Feature("revision.cite_templates", process_cite_templates,
                         returns=int, depends_on=[revision.templates])
"""
Represents number of citation templates (e.g. "Cite web") in the revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(661258898, [revision.cite_templates]))
        [175]
"""


proportion_of_templated_references = \
    cite_templates / modifiers.max(ref_tags, 1)
"""
Represents ratio of number of citation templates compared to number of
reference tags in the revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130,
        ...      [revision.proportion_of_templated_references]))
        [0.7272727272727273]
"""


def process_infobox_templates(revision_templates):
    return sum(1 for t in revision_templates if INFOBOX_RE.search(str(t.name)))

infobox_templates = Feature("revision.infobox_templates",
                            process_infobox_templates,
                            returns=int, depends_on=[revision.templates])
"""
Represents number of infobox templates (e.g. "Infobox scientist") in the
revision.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(661258898, [revision.infobox_templates]))
        [1]
"""

all = [day_of_week, hour_of_day,
       has_custom_comment, has_section_comment,
       bytes,
       chars, markup_chars, numeric_chars, symbolic_chars, uppercase_chars,
       proportion_of_markup_chars, proportion_of_numeric_chars,
       proportion_of_symbolic_chars, proportion_of_uppercase_chars,
       level_1_headings, level_2_headings, level_3_headings, level_4_headings,
       level_5_headings, level_6_headings, internal_links,
       image_links, category_links, ref_tags, templates, cite_templates,
       infobox_templates]
