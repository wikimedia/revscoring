"""
.. autoclass:: Context
    :members:
"""
from .functions import dig, draw, expand, normalize_context, solve


class Context:
    """
    Represents a contextual space for solving dependencies

    :Parameters:
        context : dict | iterable
            A set of dependents to be used in place of those already
            provided when solving dependencies.
        cache : dict
            A cache of computed values to use for every call to
            :func:`revscoring.dependencies.solve`
    """

    def __init__(self, context=None, cache=None):
        self.cache = cache if cache is not None else {}

        # Make sure context is a dict
        if context is None:
            self.context = {}
        elif not isinstance(context, dict):
            self.context = {d: d for d in context}
        else:  # else leave context alone
            self.context = context

    def solve(self, dependents, context=None, cache=None, profile=None):
        """
        Solves an iterable of dependents within the context.

        See :func:`~revscoring.dependencies.solve` for call
        signature.
        """
        context, cache = self.update_context_and_cache(context, cache)
        return solve(dependents, context=context, cache=cache, profile=profile)

    def expand(self, dependents, cache=None, context=None):
        """
        Expands iterable of all dependents within the context.

        See :func:`~revscoring.dependencies.expand` for call
        signature.
        """
        context, cache = self.update_context_and_cache(context, cache)
        return expand(dependents, context=context, cache=cache)

    def dig(self, dependents, cache=None, context=None):
        """
        Digs up the root dependents within the context.

        See :func:`~revscoring.dependencies.dig` for call signature.
        """
        context, cache = self.update_context_and_cache(context, cache)
        return dig(dependents, context=context, cache=cache)

    def draw(self, dependent, cache=None, context=None):
        """
        Returns a string representing the tree structure of a dependent's
        dependencies.

        See :func:`~revscoring.dependencies.draw` for call signature.
        """
        context, cache = self.update_context_and_cache(context, cache)
        return draw(dependent, context=context, cache=cache)

    def update(self, context=None, cache=None):
        self.context.update(normalize_context(context or {}))
        self.cache.update(cache or {})

    def update_context_and_cache(self, context, cache):
        local_context = dict(self.context)
        local_context.update(normalize_context(context or {}))

        local_cache = cache if cache is not None else {}
        local_cache.update(self.cache)
        return local_context, local_cache
