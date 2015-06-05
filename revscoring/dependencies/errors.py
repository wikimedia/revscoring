"""
.. autoclass:: DependencyError

.. autoclass:: DependencyLoop
"""

class DependencyError(RuntimeError):
    def __init__(self, message, exception):
        super().__init__(message)
        self.exception = exception

class DependencyLoop(RuntimeError):
    pass
