"""
This module provides a general set of utilities for implementing a set of
dependencies, solving them and injecting context and cache.

.. automodule:: revscoring.dependencies.dependent

functions
+++++++++
.. automodule:: revscoring.dependencies.functions

context
+++++++
.. automodule:: revscoring.dependencies.context
"""

from .context import Context
from .dependent import Dependent, DependentSet
from .functions import dig, draw, expand, normalize_context, solve

__all__ = [solve, expand, dig, draw, normalize_context, Context, Dependent,
           DependentSet]
