import sys
from importlib import import_module

sys.path.insert(0, ".")  # Necessary for working in other modules


def import_from_path(path):
    try:
        module = import_module(path)
        return module
    except ImportError:
        parts = path.split(".")
        module_path = ".".join(parts[:-1])
        attribute_name = parts[-1]

        module = import_module(module_path)

        attribute = getattr(module, attribute_name)

        return attribute


def encode(val, none_val="NULL"):
    if val is None:
        return none_val
    elif isinstance(val, bytes):
        val = str(val, 'utf-8', "replace")
    else:
        val = str(val)

    return val.replace("\t", "\\t").replace("\n", "\\n")
