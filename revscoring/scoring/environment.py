import logging
import platform
from collections import OrderedDict

from ..about import __version__
from .model_info import ModelInfo

logger = logging.getLogger(__name__)


class Environment(ModelInfo):
    """
    Constructs an environment snapshot including versions of revscoring, the
    platform, OS, etc.
    """
    def __init__(self):
        super().__init__()
        self['revscoring_version'] = __version__
        self['platform'] = platform.platform()
        self['machine'] = platform.machine()
        self['version'] = platform.version()
        self['system'] = platform.system()
        self['processor'] = platform.processor()
        self['python_build'] = platform.python_build()
        self['python_compiler'] = platform.python_compiler()
        self['python_branch'] = platform.python_branch()
        self['python_implementation'] = platform.python_implementation()
        self['python_revision'] = platform.python_revision()
        self['python_version'] = platform.python_version()
        self['release'] = platform.release()

    def check(self, raise_exception=False):
        """
        Compare the current environment with the snapshot and log warnings
        for issues.

        :Parameters:
            raise_exception : `bool`
                If True, raise and exception if the environment has any
                mismatch
        """
        current_environment = self.__class__()

        warnings = []
        for field in (self.keys() & current_environment.keys()):
            if self.get(field) != current_environment.get(field):
                warnings.append(_build_warning(
                    field, self.get(field), current_environment.get(field)))

        if len(warnings) > 0:
            message = ("Differences between the current environment " +
                       "and the environment in which the model was " +
                       "constructed environment were detected:\n" +
                       "\n".join(" - {0}".format(w) for w in warnings))
            if not raise_exception:
                logger.warn(message)
            else:
                raise RuntimeError(message)

    def lookup(self, path):
        if len(path) == 0:
            return self
        else:
            value = self[path[0]]
            if len(path) > 1:
                raise KeyError(path[1])
            else:
                return value

    def format_json(self, path_tree, **kwargs):
        fields = path_tree.keys() or self.keys()
        return OrderedDict((f, self[f]) for f in fields)

    def format_str(self, path_tree, **kwargs):
        fields = path_tree.keys() or self.keys()
        return "Environment:\n" + \
               "".join(" - {0}: {1!r}\n".format(field, self[field])
                       for field in fields)


def _build_warning(name, old, new):
    return "{0} {1!r} mismatch with original environment {2!r}" \
           .format(name, old, new)
