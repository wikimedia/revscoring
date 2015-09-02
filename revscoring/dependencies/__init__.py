"""
This module provides a general set of utilities for implementing set of
dependencies, solving then and performing injections.

.. automodule:: revscoring.dependencies.dependent

functions
+++++++++
.. automodule:: revscoring.dependencies.functions

context
+++++++
.. automodule:: revscoring.dependencies.context
"""

from .functions import solve, expand, dig, draw, normalize_context
from .context import Context
from .dependent import Dependent

__all__ = [solve, expand, dig, draw, normalize_context, Context, Dependent]
