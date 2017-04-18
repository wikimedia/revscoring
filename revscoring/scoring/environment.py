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
        warnings = []
        if self['revscoring_version'] != __version__:
            warnings.append(_build_warning(
                'revscoring version', self['revscoring_version'], __version__))

        for field in self.FIELDS:
            if self[field] != getattr(platform, field)():
                warnings.append(_build_warning(
                    field, self[field], getattr(platform, field)()))

        if len(warnings) > 0:
            message = ("Differences between the environment used to " +
                       "train the ScorerModel and the current " +
                       "environment were detected:" +
                       "\n".join(" - {0}".format(w for w in warnings)))
            logger.warn(message)

            if raise_exception:
                raise RuntimeError(message)

    def format_json(self, fields=None):
        fields = fields or self.FIELDS
        return {f: self[f] for f in fields}

    def format_str(self, fields=None):
        fields = fields or self.FIELDS
        return "".join(" - {0}: {1!r}\n".format(field, self[field])
                       for field in fields)


def _build_warning(name, old, new):
    return "{0} {1!r} mismatch with training environment {2!r}" \
           .format(name, old, new)
