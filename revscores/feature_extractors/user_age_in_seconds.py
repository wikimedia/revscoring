from mw import Timestamp

from ..datasources import revision_metadata, user_info
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[user_info, revision_metadata])
@returns(int)
def user_age_in_seconds(user_info, revision_metadata):
    
    return revision_metadata.timestamp - \
           (user_info.registration or Timestamp("20050101000000"))
