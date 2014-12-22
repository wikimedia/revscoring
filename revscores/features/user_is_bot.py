from ..datasources import user_info
from .feature import feature_processor


@feature_processor(returns=bool, depends_on=[user_info])
def user_is_bot(user_info):
    
    return "bot" in user_info.groups
