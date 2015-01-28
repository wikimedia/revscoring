import re

from ..datasources import revision_metadata
from .feature import Feature

SECTION_COMMENT_RE = re.compile(r"\/\*([^\*]|\*[^\/])+\*\/")

def process(revision_metadata):
    
    if revision_metadata.comment is not None:
        return SECTION_COMMENT_RE.match(revision_metadata.comment) is not None
    else:
        return False

is_section_comment = Feature("is_section_comment", process,
                             returns=bool, depends_on=[revision_metadata])
