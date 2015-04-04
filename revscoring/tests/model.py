from ..features import revision
from ..languages import english
from ..scorers import LinearSVCModel

revision_linearsvc = LinearSVCModel(revision.all, language=english)
