from ...datasources import revision_oriented
from ...util import NamedDict
from ..meta import aggregators


class Revision:

    def __init__(self, prefix, revision_datasources):
        self.length = aggregators.len(
            revision_datasources.bytes,
            name=prefix + ".length"
        )

        if hasattr(revision_datasources, "parent"):
            self.parent = Revision(
                prefix + ".parent",
                revision_datasources.parent
            )

revision = Revision(
    "bytes.revision",
    revision_oriented.revision
)
