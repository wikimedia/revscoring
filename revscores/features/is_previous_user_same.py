from ..datasources import previous_revision_metadata, revision_metadata
from .feature import Feature


def process(previous_revision_metadata, revision_metadata):
    
    return (previous_revision_metadata.user_id is not None and
            previous_revision_metadata.user_id ==
                    revision_metadata.user_id) or \
           previous_revision_metadata.user_text == revision_metadata.user_text

is_previous_user_same = Feature("is_previous_user_same", process,
                                returns=bool,
                                depends_on=[previous_revision_metadata,
                                            revision_metadata])
