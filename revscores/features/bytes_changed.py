from ..datasources import previous_revision_metadata, revision_metadata
from .feature import feature_processor


@feature_processor(returns=int,
                   depends_on=[previous_revision_metadata, revision_metadata])
def bytes_changed(previous_revision_metadata, revision_metadata):
    return (revision_metadata.bytes or 0) - \
           (previous_revision_metadata.bytes or 0)
