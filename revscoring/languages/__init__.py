"""
This module implements a set of :class:`~revscoring.language.Language`
-- collections of features that are language specific.

languages
+++++++++
.. automodule:: revscoring.languages.english

.. automodule:: revscoring.languages.french

.. automodule:: revscoring.languages.hebrew

.. automodule:: revscoring.languages.indonesian

.. automodule:: revscoring.languages.persian

.. automodule:: revscoring.languages.portuguese

.. automodule:: revscoring.languages.spanish
    :members:

.. automodule:: revscoring.languages.turkish
    :members:

.. automodule:: revscoring.languages.vietnamese
    :members:

Base classes
++++++++++++
.. automodule:: revscoring.languages.language

.. automodule:: revscoring.languages.space_delimited

"""
from .language import Language

__all__ = [Language]
