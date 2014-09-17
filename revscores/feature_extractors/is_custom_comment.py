import re

from ..datasources import revision_metadata
from ..util.dependencies import depends
from ..util.returns import returns
from .is_section_comment import SECTION_COMMENT_RE


@depends(on=[revision_metadata])
@returns(bool)
def is_custom_comment(revision_metadata):
    
    if revision_metadata.comment is not None:
        trimmed_comment = SECTION_COMMENT_RE.sub("", revision_metadata.comment)
        trimmed_comment = trimmed_comment.strip()
    
        return len(trimmed_comment) > 1
    else:
        return False
