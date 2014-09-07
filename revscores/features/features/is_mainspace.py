import re

from ..datasources import revision_metadata
from ..dependencies import depends_on


@depends_on(revision_metadata)
def is_mainspace(revision_metadata):
    
    return revision_metadata.page_namespace == 0
