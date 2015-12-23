from . import datasources
from ...datasources import revision_oriented
from .features import Revision

prefix = "wikitext.revision"

revision = Revision(
    prefix,
    datasources.Revision(prefix, revision_oriented.revision)
)
