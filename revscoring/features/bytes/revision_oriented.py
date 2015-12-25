from . import datasources
from ...datasources import revision_oriented
from ..meta import aggregators

prefix = "bytes.revision"


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
    prefix,
    datasources.Revision(prefix, revision_oriented.revision)
)
