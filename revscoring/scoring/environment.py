import logging
import platform

from ..about import __version__

logger = logging.getLogger(__name__)


class Environment(dict):
    FIELDS = ['platform', 'machine', 'version', 'system', 'processor',
              'python_build', 'python_compiler', 'python_branch',
              'python_implementation', 'python_revision',
              'python_version', 'release']

    def __init__(self):
        """
        Construct an environment snapshot.
        """
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
        warnings = []
        if self['revscoring_version'] != __version__:
            warnings.append(_build_warning(
                'revscoring version', self['revscoring_version'], __version__))

        for field in self.FIELDS:
            if self[field] != getattr(platform, field)():
                warnings.append(_build_warning(
                    field, self[field], getattr(platform, field)()))

        if len(warnings) > 0:
            message = ("Differences between the current environment " +
                       "and the environment in which the model was " +
                       "constructed environment were detected:\n" +
                       "\n".join(" - {0}".format(w) for w in warnings))
            if not raise_exception:
                logger.warn(message)
            else:
                raise RuntimeError(message)

    def format_json(self, fields=None):
        fields = fields or self.FIELDS
        return {f: self[f] for f in fields}

    def format_str(self, fields=None):
        fields = fields or self.FIELDS
        return "".join(" - {0}: {1!r}\n".format(field, self[field])
                       for field in fields)


def _build_warning(name, old, new):
    return "{0} {1!r} mismatch with original environment {2!r}" \
           .format(name, old, new)
