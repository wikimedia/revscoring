from ..datasources import previous_revision_metadata, revision_metadata
from .feature import feature_processor


@feature_processor(returns=int,
                   depends_on=[previous_revision_metadata, revision_metadata])
def seconds_since_last_page_edit(previous_revision_metadata, revision_metadata):
    
    return revision_metadata.timestamp - \
           (previous_revision_metadata.timestamp or
            revision_metadata.timestamp)
