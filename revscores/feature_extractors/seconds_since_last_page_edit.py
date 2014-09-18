from ..datasources import previous_revision_metadata, revision_metadata
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[previous_revision_metadata, revision_metadata])
@returns(int)
def seconds_since_last_page_edit(previous_revision_metadata, revision_metadata):
    
    return revision_metadata.timestamp - previous_revision_metadata.timestamp
