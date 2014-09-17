import re

from ..datasources import revision_metadata
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[revision_metadata])
@returns(bool)
def is_mainspace(revision_metadata):
    
    return revision_metadata.page_namespace == 0
