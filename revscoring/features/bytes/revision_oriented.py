from ...datasources import revision_oriented
from ...util import NamedDict
from ..meta import aggregators


class Revision:

    def __init__(self, prefix, revision_bytes, parent_revision_bytes=None):
        self.length = aggregators.len(
            revision_bytes,
            name=prefix + ".length"
        )

        if parent_revision_bytes is not None:
            self.parent = Revision(
                prefix + ".parent",
                parent_revision_bytes
            )

revision = Revision(
    "bytes.revision",
    revision_oriented.revision.bytes,
    revision_oriented.revision.parent.bytes
)
