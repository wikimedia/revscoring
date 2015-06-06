"""
This module implements a set of :class:`~revscoring.languages.language.Language`
for use in the extraction of language-dependent features.  A language generally
implements 4 :class:`~revscoring.languages.language.LanguageUtility`:

* :data:`~revscoring.languages.language.stem_word`
* :data:`~revscoring.languages.language.is_badword`
* :data:`~revscoring.languages.language.is_misspelled`
* :data:`~revscoring.languages.language.is_stopword`

A growing set of :class:`~revscoring.languages.language.Language` are provided
as part of the common installation.

english
+++++++
.. automodule:: revscoring.languages.english
    :members:

french
++++++
.. automodule:: revscoring.languages.french
    :members:

persian
+++++++
.. automodule:: revscoring.languages.persian
    :members:

portuguese
++++++++++
.. automodule:: revscoring.languages.portuguese
    :members:

turkish
+++++++
.. automodule:: revscoring.languages.turkish
    :members:

language
++++++++++++++++++
.. automodule:: revscoring.languages.language
"""

from .language import Language, LanguageUtility
from .language import stem_word, is_badword, is_misspelled, is_stopword
from .english import english
from .portuguese import portuguese
from .turkish import turkish
from .french import french
from .persian import persian
