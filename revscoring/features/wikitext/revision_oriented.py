from revscoring.datasources import revision_oriented

from . import datasources
from .features import Revision

name = "wikitext.revision"

revision = Revision(
    name,
    datasources.Revision(name, revision_oriented.revision)
)
