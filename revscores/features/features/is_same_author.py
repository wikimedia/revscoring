import re

from ..datasources import previous_revision_metadata, revision_metadata
from ..dependencies import depends_on


@depends_on(previous_revision_metadata, revision_metadata)
def is_same_author(previous_revision_metadata, revision_metadata):
    
    return previous_revision_metadata.user_text == revision_metadata.user_text
