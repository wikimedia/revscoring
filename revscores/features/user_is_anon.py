import re

from ..datasources import revision_metadata
from .feature import feature_processor


@feature_processor(returns=bool, depends_on=[revision_metadata])
def user_is_anon(revision_metadata):
    
    return revision_metadata.user_id == 0 or revision_metadata.user_id is None
