from ..datasources import previous_user_revision_metadata, revision_metadata
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[previous_user_revision_metadata, revision_metadata])
@returns(int)
def seconds_since_last_user_edit(previous_user_revision_metadata,
                                 revision_metadata):
    
    return revision_metadata.timestamp - \
           (previous_user_revision_metadata.timestamp or
            revision_metadata.timestamp)
