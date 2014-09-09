import re

from ..datasources import revision_metadata
from ..util.dependencies import depends


@depends(on=[revision_metadata])
def is_anon(revision_metadata):
    
    return revision_metadata.user_id == 0 or revision_metadata.user_id is None
