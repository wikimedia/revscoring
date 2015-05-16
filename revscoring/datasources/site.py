from .datasource import Datasource


def process_namespace_map():
    raise NotImplementedError()
namespace_map = Datasource("site.namespace_map", process_namespace_map)
