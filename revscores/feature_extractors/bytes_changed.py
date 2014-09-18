from ..datasources import previous_revision_metadata, revision_metadata
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[previous_revision_metadata, revision_metadata])
@returns(int)
def bytes_changed(previous_revision_metadata, revision_metadata):
    
    return (revision_metadata.bytes or 0) - \
           (previous_revision_metadata.bytes or 0)
