import re

from ..datasources import revision_metadata
from .feature import feature_processor


@feature_processor(returns=bool, depends_on=[revision_metadata])
def is_mainspace(revision_metadata):
    
    return revision_metadata.page_namespace == 0
