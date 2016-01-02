from . import datasources
from ...datasources import revision_oriented
from .features import Revision

name = "wikitext.revision"

revision = Revision(
    name,
    datasources.Revision(name, revision_oriented.revision)
)
"""
Represents the base revision of interest.  Implements this a basic structure:

* revision: :class:`~revscoring.features.wikibase.Revision`
    * parent: :class:`~revscoring.features.wikibase.Revision`
    * diff: :class:`~revscoring.features.wikibase.Diff`
"""  # noqa
