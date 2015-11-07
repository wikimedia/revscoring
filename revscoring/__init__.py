"""
This library contains a set of facilities for constructing and applying
:class:`~revscoring.ScorerModel` s to MediaWiki revisions. This library
eases the training and testing of Machine Learning-based scoring
strategies.

* See the :ref:`API reference <api-reference>` for detailed information

Key Features
------------

Scorer Models
+++++++++++++
:class:`~revscoring.ScorerModel` are the core of
the `revscoring` system.  Provide a simple interface with complex
internals.  Most commonly, a :class:`revscoring.scorer_models.MLScorerModel`
(Machine Learned) is
:meth:`~revscoring.scorer_models.MLScorerModel.train`'d and
:meth:`~revscoring.scorer_models.MLScorerModel.test`'d on
labeled data to provide a basis for scoring.
We currently support
:mod:`Support Vector Classifier <revscoring.scorer_models.svc>`,
:mod:`Random Forest <revscoring.scorer_models.rf>`, and
:mod:`Naive Bayes <revscoring.scorer_models.nb>`
type models. See :mod:`revscoring.scorer_models`

Example:
    >>> import mwapi
    >>> from revscoring import ScorerModel
    >>> from revscoring.extractors import APIExtractor
    >>>
    >>> with open("models/enwiki.damaging.linear_svc.model") as f:
    ...     scorer_model = ScorerModel.load(f)
    ...
    >>> extractor = APIExtractor(mwapi.Session(host="https://en.wikipedia.org",
    ...                                        user_agent="revscoring demo"))
    >>>
    >>> feature_values = extractor.extract(123456789, scorer_model.features)
    >>>
    >>> print(scorer_model.score(feature_values))
    {'prediction': True,
     'probability': {False: 0.4694409344514984,
                     True: 0.5305590655485017}}

Feature extraction
++++++++++++++++++
Revscoring provides a dependency-injection-based feature extraction
framework that allows new features to be built on top of old.  This allows
a powerful means to expressing new features and a simple way to address
efficiency concerns. See :mod:`revscoring.features`,
:mod:`revscoring.datasources`, and :mod:`revscoring.extractors`

Example:

    >>> import mwapi
    >>> from revscoring.extractors import APIExtractor
    >>> from revscoring.features import diff, user
    >>>
    >>> features = [diff.bytes_changed, user.is_bot]
    >>> extractor = APIExtractor(mwapi.Session(host="https://en.wikipedia.org",
    ...                                        user_agent="revscoring demo"))
    >>>
    >>> feature_values = extractor.extract(123456789, features)
    >>>
    >>> print([(f, v) for f, v in zip(features, feature_values)])
    [(<(revision.bytes - parent_revision.bytes)>, 2),
     (<user.is_bot>, False)]

Language support
++++++++++++++++
Many features require language specific utilities to be available to
support feature extraction.  In order to support this, we provide a
collection of language feature sets that work like other features except
that they are language-specific.  Language-specific feature sets are
available for the following languages:
:data:`~revscoring.languages.dutch`,
:data:`~revscoring.languages.english`,
:data:`~revscoring.languages.french`,
:data:`~revscoring.languages.german`,
:data:`~revscoring.languages.hebrew`,
:data:`~revscoring.languages.indonesian`,
:data:`~revscoring.languages.italian`,
:data:`~revscoring.languages.persian`,
:data:`~revscoring.languages.portuguese`,
:data:`~revscoring.languages.spanish`,
:data:`~revscoring.languages.turkish`, and
:data:`~revscoring.languages.vietnamese`.
See :mod:`revscoring.languages`

Example:

    >>> from revscoring.datasources import revision
    >>> from revscoring.dependencies import solve
    >>> from revscoring.languages import spanish, english
    >>>
    >>> features = [english.revision.informals, spanish.revision.informals]
    >>> feature_values = solve(features,
    ...                        cache={revision.text: "I think it is stupid."})
    >>>
    >>> print([(f, v) for f, v in zip(features, feature_values)])
    [(<revscoring.languages.english.revision.informals>, 2),
     (<revscoring.languages.spanish.revision.informals>, 0)]
"""
from .datasources import Datasource
from .dependencies import Dependent
from .extractors import Extractor
from .features import Feature
from .languages import Language
from .scorer_models import ScorerModel

__version__ = "0.7.2"

__all__ = [Datasource, Dependent, Extractor, Feature, Language, ScorerModel]
