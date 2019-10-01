from revscoring.datasources import revision_oriented, session_oriented
from revscoring.dependencies import DependentSet

from . import datasources
from .revision_oriented import Revision

name = "bytes.session"


class Session(DependentSet):
    def __init__(self, name):
        super().__init__(name)
        revision = Revision(
            name, datasources.Revision(name, revision_oriented.revision))
        self.revisions = session_oriented.list_of_tree(
            revision, rewrite_name=session_oriented.rewrite_name,
            cache={d: d for d in session_oriented.session})


session = Session(name)
