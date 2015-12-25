from datetime import datetime

import mwtypes
from pytz import utc

from ...datasources import revision_oriented
from ..feature import Feature

MW_REGISTRATION_EPOCH = mwtypes.Timestamp("2006-01-01T00:00:00Z")


class Revision:

    def __init__(self, prefix, revision_datasources):
        self.prefix = prefix
        self.datasources = revision_datasources

        self.day_of_week = Feature(
            prefix + ".day_of_week", _process_day_of_week,
            returns=int,
            depends_on=[revision_datasources.timestamp]
        )
        """
        Represents day of week when the edit was made in UTC.
        """

        self.hour_of_day = Feature(
            prefix + ".hour_of_day", _process_hour_of_day,
            returns=int,
            depends_on=[revision_datasources.timestamp]
        )
        """
        Represents hour of day when the edit was made in UTC.
        """

        if hasattr(revision_datasources, "parent"):
            self.parent = ParentRevision(
                prefix + ".parent",
                revision_datasources
            )

        if hasattr(revision_datasources, "page") and \
           hasattr(revision_datasources.page, "creation"):
            self.page = Page(
                prefix + ".page",
                revision_datasources
            )

        if hasattr(revision_datasources, "user") and \
           hasattr(revision_datasources.user, "info"):
            self.user = User(
                prefix + ".user",
                revision_datasources
            )


class ParentRevision(Revision):
    def __init__(self, prefix, revision_datasources):
        super().__init__(prefix, revision_datasources.parent)

        self.seconds_since = Feature(
            prefix + ".seconds_since",
            _process_seconds_since,
            returns=int,
            depends_on=[revision_datasources.parent.timestamp,
                        revision_datasources.timestamp])


class User:
    def __init__(self, prefix, revision_datasources):

        self.prefix = prefix
        self.datasources = revision_datasources.user

        if hasattr(self.datasources, 'info'):
            self.seconds_since_registration = Feature(
                prefix + ".seconds_since_registration",
                _process_seconds_since_registration,
                returns=int,
                depends_on=[revision_datasources.user.id,
                            revision_datasources.user.info.registration,
                            revision_datasources.timestamp])

        if hasattr(self.datasources, 'last_revision'):
            self.last_revision = LastUserRevision(
                prefix + ".last_revision",
                revision_datasources
            )


class LastUserRevision(Revision):
    def __init__(self, prefix, revision_datasources):
        super().__init__(prefix, revision_datasources.user.last_revision)

        self.seconds_since = Feature(
            prefix + ".seconds_since",
            _process_seconds_since,
            returns=int,
            depends_on=[revision_datasources.user.last_revision.timestamp,
                        revision_datasources.timestamp])


class Page:
    def __init__(self, prefix, revision_datasources):
        self.creation = PageCreation(
            prefix + ".creation",
            revision_datasources
        )


class PageCreation:
    def __init__(self, prefix, revision_datasources):
        self.seconds_since = Feature(
            prefix + ".seconds_since",
            _process_seconds_since,
            returns=int,
            depends_on=[revision_datasources.page.creation.timestamp,
                        revision_datasources.timestamp])


def _process_day_of_week(timestamp):
    dt = datetime.fromtimestamp(timestamp.unix(), tz=utc)
    return dt.weekday()


def _process_hour_of_day(timestamp):
    dt = datetime.fromtimestamp(timestamp.unix(), tz=utc)
    return dt.hour


def _process_seconds_since(old_timestamp, current_timestamp):
    if old_timestamp is None:
        return 0
    else:
        return current_timestamp - old_timestamp


def _process_seconds_since_registration(id, registration, timestamp):
    if id is None:  # User is anon
        return 0
    else:
        # Handles users who registered before registration dates were
        # recorded
        registration = registration or MW_REGISTRATION_EPOCH
        print(registration)

        return _process_seconds_since(registration, timestamp)


revision = Revision("temporal.revision", revision_oriented.revision)
