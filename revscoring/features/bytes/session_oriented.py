from revscoring.datasources import session_oriented
from revscoring.dependencies import DependentSet

from . import datasources
from .revision_oriented import Revision

name = "bytes.session"


class Session(DependentSet):
    """
    Represents an editor's activity session
    """
    def __init__(self, name, revisions_datasources):
        super().__init__(name)
        revision = Revision(
            name, datasources.Revision(name, revisions_datasources))
        self.revisions = session_oriented.list_of_tree(
            revision, rewrite_name=session_oriented.rewrite_name,
            cache={d.name: d for d in revisions_datasources})
        """
        :class:`~revscoring.datasources.meta.expanders.list_of`(:class:`~revscoring.features.bytes.Revision`) :
        The revisions saved by the users within the session.
        """

session = Session(name, session_oriented.session.revisions)
