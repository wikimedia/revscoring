from mw import Timestamp

from ..datasources import revision_metadata, user_info
from .feature import feature_processor


@feature_processor(returns=int, depends_on=[user_info, revision_metadata])
def user_age_in_seconds(user_info, revision_metadata):
    
    return revision_metadata.timestamp - \
           (user_info.registration or Timestamp("20050101000000"))
