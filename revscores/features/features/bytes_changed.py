import re

from ..datasources import previous_revision_metadata, revision_metadata
from ..dependencies import depends_on

SECTION_COMMENT_RE = re.compile(r"\/\*([^\*]|\*[^\/])+\*\/")

@depends_on(previous_revision_metadata, revision_metadata)
def bytes_changed(previous_revision_metadata, revision_metadata):
    
    return previous_revision_metadata.bytes - revision_metadata.bytes
