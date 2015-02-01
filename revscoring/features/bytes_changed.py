from ..datasources import previous_revision_metadata, revision_metadata
from .feature import Feature


def process(previous_revision_metadata, revision_metadata):
    return (revision_metadata.bytes or 0) - \
           (previous_revision_metadata.bytes or 0)

bytes_changed = Feature("bytes_changed", process, returns=int,
                        depends_on=[previous_revision_metadata,
                                    revision_metadata])
