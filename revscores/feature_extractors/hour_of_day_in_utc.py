from datetime import datetime

from pytz import utc

from ..datasources import revision_metadata
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[revision_metadata])
@returns(int)
def hour_of_day_in_utc(revision_metadata):
    
    dt = datetime.fromtimestamp(revision_metadata.timestamp.unix(), tz=utc)
    return dt.hour
