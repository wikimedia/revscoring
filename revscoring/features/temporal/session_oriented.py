from revscoring import Feature
from revscoring.datasources import session_oriented
from revscoring.datasources.meta.selectors import first
from revscoring.dependencies import DependentSet

from .revision_oriented import (Revision, _process_seconds_since,
                                _process_seconds_since_registration)

name = "temporal.session"


class Session(DependentSet):
    """
    Represents an editor's activity session
    """
    def __init__(self, name, revisions_datasources):
        super().__init__(name)
        session_revision = Revision(
            name + ".revisions", revisions_datasources)
        self.revisions = session_oriented.list_of_tree(
            session_revision, rewrite_name=session_oriented.rewrite_name,
            cache={d.name: d for d in revisions_datasources})
        """
        :class:`~revscoring.datasources.meta.expanders.list_of`(:class:`~revscoring.features.temporal.Revision`) :
        The revisions saved by the users within the session.
        """

        self.user = SessionUser(
            name + ".user", session_oriented.session.user,
            revisions_datasources)
        """
        :class:`~revscoring.features.temporal.session_oriented.SessionUser` :
        The session user.
        """


class SessionUser(DependentSet):
    "Represents a session user"

    def __init__(self, name, user_datasources, revisions_datasources):
        super().__init__(name)
        self.datasources = user_datasources

        if hasattr(self.datasources, 'info'):
            self.seconds_since_registration = Feature(
                name + ".seconds_since_registration",
                _process_seconds_since_registration,
                returns=int,
                depends_on=[self.datasources.id,
                            self.datasources.info.registration,
                            first(revisions_datasources.timestamp)])
            """
            `int` : The number of seconds since the user registered their
            account -- or zero in the case of anons -- before the start of the
            current session.  If the user has a registration date that is
            *after* the revision timestamp (should be implossible, but happens
            sometimes), the user is assumed to be 1 year old.
            """

        if hasattr(self.datasources, 'last_revision'):
            self.last_revision = LastSessionUserRevision(
                name + ".last_revision", user_datasources,
                revisions_datasources)
            """
            :class:`~revscoring.features.temporal.session_oriented.LastSessionUserRevision` :
            The last revision saved by the user before the start of the session.
            """


class LastSessionUserRevision(Revision):
    "Represents a revision user's last revision before the start of the session"

    def __init__(self, name, user_datasources, revisions_datasources):
        super().__init__(name, user_datasources.last_revision)

        self.seconds_since = Feature(
            name + ".seconds_since",
            _process_seconds_since,
            returns=int,
            depends_on=[user_datasources.last_revision.timestamp,
                        first(revisions_datasources.timestamp)])
        """
        `int`: The number of seconds since the user last saved an edit before
        the start of the current session.
        """


session = Session(name, session_oriented.session.revisions)
