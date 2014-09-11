import re

from ..datasources import previous_revision_metadata, revision_metadata
from ..util.dependencies import depends

SECTION_COMMENT_RE = re.compile(r"\/\*([^\*]|\*[^\/])+\*\/")

@depends(on=[previous_revision_metadata, revision_metadata])
def bytes_changed(previous_revision_metadata, revision_metadata):
    
    return (revision_metadata.bytes or 0) - \
           (previous_revision_metadata.bytes or 0)
