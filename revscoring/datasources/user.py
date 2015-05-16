from . import revision
from .datasource import Datasource
from .types import UserInfo


def process_info():
    raise NotImplementedError()

info = Datasource("user.info", process_info, depends_on=[])
