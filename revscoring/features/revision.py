from datetime import datetime

from pytz import utc

from ..datasources import revision
from .feature import Feature
from .meta import string_matches
from .util import SECTION_COMMENT_RE


# ############################### Time ########################################

def process_day_of_week(revision_metadata):

    dt = datetime.fromtimestamp(revision_metadata.timestamp.unix(), tz=utc)
    return dt.weekday()

day_of_week = Feature("revision.day_of_week", process_day_of_week,
                      returns=int, depends_on=[revision.metadata])
"""
Represents day of week when the edit was made in UTC.
"""


def process_hour_of_day(revision_metadata):

    dt = datetime.fromtimestamp(revision_metadata.timestamp.unix(), tz=utc)
    return dt.hour

hour_of_day = Feature("revision.hour_of_day", process_hour_of_day,
                      returns=int, depends_on=[revision.metadata])
"""
Represents hour of day when the edit was made in UTC.
"""


# ############################### Comment #####################################
def comment_matches(regex, name=None):
    return string_matches(regex, revision.comment, name=name)

has_section_comment = comment_matches(
    SECTION_COMMENT_RE,
    name="revision.has_section_comment"
)
"""
Represents whether the edit has section edit summary.

Section edit summaries are like ``"/* <section title> */"`` which mediawiki
automatically creates them when a user edit a section.
"""

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
"""
