import re

from ..datasources import revision_metadata
from .feature import feature_processor
from .is_section_comment import SECTION_COMMENT_RE


@feature_processor(returns=bool, depends_on=[revision_metadata])
def is_custom_comment(revision_metadata):
    
    if revision_metadata.comment is not None:
        trimmed_comment = SECTION_COMMENT_RE.sub("", revision_metadata.comment)
        trimmed_comment = trimmed_comment.strip()
    
        return len(trimmed_comment) > 1
    else:
        return False
