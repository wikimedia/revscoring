from . import datasources
from ...datasources import revision_oriented
from .features import Revision

name = "wikitext.revision"

revision = Revision(
    name,
    datasources.Revision(name, revision_oriented.revision)
)
