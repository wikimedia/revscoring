"""
.. autoclass:: DependencyError

.. autoclass:: CaughtDependencyError

.. autoclass:: DependencyLoop

.. autoclass:: MissingResource

.. autoclass:: RevisionNotFound

.. autoclass:: PageNotFound

.. autoclass:: UserNotFound

.. autoclass:: UserDeleted

.. autoclass:: CommentDeleted

.. autoclass:: TextDeleted
"""


class DependencyError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return "{0}: {1}".format(self.__class__.__name__, self.message)


class CaughtDependencyError(DependencyError):

    def __init__(self, message, exception=None, tb=None,
                 formatted_exception=None):
        super().__init__(message)
        self.exception = exception
        self.tb = tb
        self.formatted_exception = formatted_exception

    def __str__(self):
        class_name = self.exception.__class__.__name__
        return "{0}: {1}\n{2}".format(class_name, self.message,
                                      self.formatted_exception)


class DependencyLoop(DependencyError):
    pass


class MissingResource(DependencyError):
    pass


class RevisionNotFound(MissingResource):
    def __init__(self, datasources, rev_id=None, arg=None):
        super().__init__("Could not find revision ({0}:{1})"
                         .format(datasources, repr(rev_id)))


class UserNotFound(MissingResource):
     def __init__(self, datasources, user_text=None, arg=None):
         super().__init__("Could not find user account ({0}:{1})"
                          .format(datasources, repr(user_text)))


class PageNotFound(MissingResource):
     def __init__(self, datasources, page_id=None, arg=None):
         super().__init__("Could not find page ({0}:{1})"
                          .format(datasources, repr(page_id)))


class UserDeleted(MissingResource):
     def __init__(self, datasources, arg=None):
         super().__init__("User deleted ({0})"
                          .format(datasources))


class CommentDeleted(MissingResource):
     def __init__(self, datasources, arg=None):
         super().__init__("Comment deleted ({0})"
                          .format(datasources))


class TextDeleted(MissingResource):
    def __init__(self, datasources, arg=None):
        super().__init__("Text deleted ({0})"
                         .format(datasources))
