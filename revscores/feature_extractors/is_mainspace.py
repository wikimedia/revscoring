import re

from ..datasources import revision_metadata
from ..util.dependencies import depends


@depends(on=[revision_metadata])
def is_mainspace(revision_metadata):
    
    return revision_metadata.page_namespace == 0
