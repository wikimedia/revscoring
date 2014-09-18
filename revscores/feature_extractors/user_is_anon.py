import re

from ..datasources import revision_metadata
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[revision_metadata])
@returns(bool)
def user_is_anon(revision_metadata):
    
    return revision_metadata.user_id == 0 or revision_metadata.user_id is None
