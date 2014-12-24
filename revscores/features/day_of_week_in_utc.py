from datetime import datetime

from pytz import utc

from ..datasources import revision_metadata
from .feature import Feature


def process(revision_metadata):
    
    dt = datetime.fromtimestamp(revision_metadata.timestamp.unix(), tz=utc)
    return dt.weekday()

day_of_week_in_utc = Feature("day_of_week_in_utc", process,
                             returns=int, depends_on=[revision_metadata])
