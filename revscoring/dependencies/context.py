"""
.. autoclass:: Context
    :members:
"""
from .functions import dig, draw, expand, solve


class Context:
    """
    Represents a contextual space for solving dependencies

    :Parameters:
        context : dict | iterable
            A set of dependents to be used in place of those already
            provided when solving dependencies.
        cache : dict
            A cache of computed values to use for every call to `solve()`
    """
    def __init__(self, context=None, cache=None):
        self.cache = cache or {}

        # Make sure context is a dict
        if context is None:
            self.context = {}
        elif not isinstance(context, dict):
            self.context = {d: d for d in context}
        else:  # else leave context alone
            self.context = context

    def solve(self, dependents, context=None, cache=None):
        """
        Solves an iterable of dependents within the context.

        See :func:`~revscoring.dependencies.functions.solve` for call
        signature.
        """
        context, cache = self.update_context_and_cache(context, cache)
        return solve(dependents, context=context, cache=cache)

    def expand(self, dependents, cache=None, context=None):
        """
        Expands iterable of all dependents within the context.

        See :func:`~revscoring.dependencies.functions.expand` for call
        signature.
        """
        context, cache = self.update_context_and_cache(context, cache)
        return expand(dependents, context=context, cache=cache)

    def dig(self, dependents, cache=None, context=None):
        """
        Digs up the root dependents within the context.

        See :func:`~revscoring.dependencies.functions.dig` for call signature.
        """
        context, cache = self.update_context_and_cache(context, cache)
        return dig(dependents, context=context, cache=cache)

    def draw(self, dependent, cache=None, context=None):
        """
        Returns a string representing the tree structure of a dependent's
        dependencies.

        See :func:`~revscoring.dependencies.functions.draw` for call signature.
        """
        context, cache = self.update_context_and_cache(context, cache)
        return draw(dependent, context=context, cache=cache)

    def update_context_and_cache(self, context, cache):
        new_context = {}  # Prepare context
        new_context.update(self.context)  # Load extractor context
        new_context.update(context or {})  # Load call context

        new_cache = {}  # Prepare cache
        new_cache.update(self.cache)  # Load cache for extractor
        new_cache.update(cache or {})  # Load call cache

        return new_context, new_cache
