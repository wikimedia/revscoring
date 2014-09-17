import re

from ..datasources import previous_revision_metadata, revision_metadata
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[previous_revision_metadata, revision_metadata])
@returns(bool)
def is_previous_user_same(previous_revision_metadata, revision_metadata):
    
    return previous_revision_metadata.user_text == revision_metadata.user_text
