from datetime import datetime

from pytz import utc

from ..datasources import revision_metadata
from .feature import feature_processor


@feature_processor(returns=int, depends_on=[revision_metadata])
def day_of_week_in_utc(revision_metadata):
    
    dt = datetime.fromtimestamp(revision_metadata.timestamp.unix(), tz=utc)
    return dt.weekday()
