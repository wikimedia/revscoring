import re

from ..datasources import revision_metadata
from ..util.dependencies import depends
from ..util.returns import returns

SECTION_COMMENT_RE = re.compile(r"\/\*([^\*]|\*[^\/])+\*\/")

@depends(on=[revision_metadata])
@returns(bool)
def is_section_comment(revision_metadata):
    
    if revision_metadata.comment is not None:
        return SECTION_COMMENT_RE.match(revision_metadata.comment) is not None
    else:
        return False
