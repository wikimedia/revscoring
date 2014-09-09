import re

from ..datasources import revision_metadata
from ..util.dependencies import depends_on


@depends_on(revision_metadata)
def is_anon(revision_metadata):
    
    return revision_metadata.user_id == 0 or revision_metadata.user_id is None
