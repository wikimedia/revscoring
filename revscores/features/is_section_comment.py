import re

from ..datasources import revision_metadata
from .feature import feature_processor

SECTION_COMMENT_RE = re.compile(r"\/\*([^\*]|\*[^\/])+\*\/")

@feature_processor(returns=bool, depends_on=[revision_metadata])
def is_section_comment(revision_metadata):
    
    if revision_metadata.comment is not None:
        return SECTION_COMMENT_RE.match(revision_metadata.comment) is not None
    else:
        return False
