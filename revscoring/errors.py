"""
.. autoclass:: DependencyError

.. autoclass:: CaughtDependencyError

.. autoclass:: DependencyLoop

.. autoclass:: MissingResource

.. autoclass:: RevisionNotFound
"""


class DependencyError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return "{0}: {1}".format(self.__class__.__name__, self.message)


class CaughtDependencyError(DependencyError):

    def __init__(self, message, exception=None, tb=None):
        super().__init__(message)
        self.exception = exception
        self.tb = tb

    def __str__(self):
        class_name = self.exception.__class__.__name__
        return "{0}: {1}".format(class_name, self.message)

    def __getnewargs__(self):
        return (self.message, self.exception, self.tb)


class DependencyLoop(DependencyError):
    pass


class MissingResource(DependencyError):
    pass


class RevisionNotFound(MissingResource):
    def __init__(self, arg=None):
        super().__init__("Could not locate revision. " +
                         "It may have been deleted.")
