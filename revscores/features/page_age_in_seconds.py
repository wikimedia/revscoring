from ..datasources import first_revision_metadata, revision_metadata
from .feature import feature_processor


@feature_processor(returns=int,
                   depends_on=[first_revision_metadata, revision_metadata])
def page_age_in_seconds(first_revision_metadata, revision_metadata):
    
    return revision_metadata.timestamp - first_revision_metadata.timestamp
