"""
This library contains a set of facilities for constructing and applying
:class:`~revscoring.Model` s to MediaWiki revisions. This library
eases the training and testing of Machine Learning-based scoring
strategies.

* See the :ref:`API reference <api-reference>` for detailed information.

Key Features
------------

Scoring Models
++++++++++++++
Scoring :class:`~revscoring.Model` are the core of
the `revscoring` system.  Provide a simple interface with complex
internals.  Most commonly, a :class:`~revscoring.scoring.models.Learned`
(Machine Learned) is
:meth:`~revscoring.scoring.models.Learned.train`'d and
:meth:`~revscoring.Model.test`'d on
labeled data to provide a basis for scoring.
We currently support
:mod:`Gradient Boosting <revscoring.scoring.models.gradient_boosting>`,
:mod:`Random Forest <revscoring.scoring.models.random_forest>`,
:mod:`Linear Regression <revscoring.scoring.models.linear>`,
:mod:`Support Vector Classifier <revscoring.scoring.models.svc>`, and
:mod:`Naive Bayes <revscoring.scoring.models.naive_bayes>`
type models. See :mod:`revscoring.scoring`

Example:
    >>> import mwapi
    >>> from revscoring import Model
    >>> from revscoring.extractors import api
    >>>
    >>> with open("models/enwiki.damaging.linear_svc.model") as f:
    ...     model = Model.load(f)
    ...
    >>> extractor = api.Extractor(mwapi.Session(host="https://en.wikipedia.org",
    ...                                         user_agent="revscoring demo"))
    >>> values = extractor.extract(123456789, model.features)
    >>> print(model.score(values))
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

    >>>     >>> from mwapi import Session
    >>> from revscoring.extractors import api
    >>> from revscoring.features import temporal, wikitext
    >>>
    >>> session = Session("https://en.wikipedia.org/w/api.php", user_agent="test")
    >>> api_extractor = api.Extractor(session)
    >>>
    >>> features = [temporal.revision.day_of_week,
    ...             temporal.revision.hour_of_day,
    ...             wikitext.revision.parent.headings_by_level(2)]
    >>>
    >>> values = api_extractor.extract(624577024, features)
    >>> for feature, value in zip(features, values):
    ...     print("\t{0}: {1}".format(feature, repr(value)))
    ...
        <temporal.revision.day_of_week>: 6
        <temporal.revision.hour_of_day>: 19
        <wikitext.revision.parent.headings_by_level(2)>: 5


Language support
++++++++++++++++
Many features require language specific utilities to be available to
support feature extraction.  In order to support this, we provide a
collection of language feature sets that work like other features except
that they are language-specific.  Language-specific feature sets are
available for the following languages:
:data:`~revscoring.languages.albanian`,
:data:`~revscoring.languages.arabic`,
:data:`~revscoring.languages.bengali`,
:data:`~revscoring.languages.bosnian`,
:data:`~revscoring.languages.catalan`,
:data:`~revscoring.languages.chinese`,
:data:`~revscoring.languages.croatian`,
:data:`~revscoring.languages.czech`,
:data:`~revscoring.languages.dutch`,
:data:`~revscoring.languages.english`,
:data:`~revscoring.languages.estonian`,
:data:`~revscoring.languages.finnish`,
:data:`~revscoring.languages.french`,
:data:`~revscoring.languages.galician`,
:data:`~revscoring.languages.german`,
:data:`~revscoring.languages.greek`,
:data:`~revscoring.languages.hebrew`,
:data:`~revscoring.languages.hindi`,
:data:`~revscoring.languages.hungarian`,
:data:`~revscoring.languages.icelandic`,
:data:`~revscoring.languages.indonesian`,
:data:`~revscoring.languages.italian`,
:data:`~revscoring.languages.japanese`,
:data:`~revscoring.languages.korean`,
:data:`~revscoring.languages.latvian`,
:data:`~revscoring.languages.norwegian`,
:data:`~revscoring.languages.persian`,
:data:`~revscoring.languages.polish`,
:data:`~revscoring.languages.portuguese`,
:data:`~revscoring.languages.romanian`,
:data:`~revscoring.languages.russian`,
:data:`~revscoring.languages.spanish`,
:data:`~revscoring.languages.swedish`,
:data:`~revscoring.languages.tamil`,
:data:`~revscoring.languages.turkish`,
:data:`~revscoring.languages.ukrainian`, and
:data:`~revscoring.languages.vietnamese`.
See :mod:`revscoring.languages`

Example:

    >>> from revscoring.datasources.revision_oriented import revision
    >>> from revscoring.dependencies import solve
    >>> from revscoring.languages import english, spanish
    >>>
    >>> features = [english.informals.revision.matches,
    ...              spanish.informals.revision.matches]
    >>> values = solve(features, cache={revision.text: "I think it is stupid."})
    >>>
    >>> for feature, value in zip(features, values):
    ...     print("\t{0}: {1}".format(feature, repr(value)))
    ...
        <len(<english.informals.revision.matches>)>: 2
        <len(<spanish.informals.revision.matches>)>: 0
"""  # noqa
import platform
import sys

from pkg_resources import VersionConflict

from .about import (__author__, __author_email__, __description__, __name__,
                    __url__, __version__)
from .datasources import Datasource
from .dependencies import Dependent, DependentSet
from .extractors import Extractor
from .features import Feature, FeatureVector
from .score_processor import ScoreProcessor
from .scoring import Model

if sys.version_info <= (3, 0):
    raise VersionConflict(
        "Revscoring requires Python '>=3' " +
        "but your Python version is " +
        platform.python_version())


__all__ = [Datasource, Dependent, DependentSet, Extractor, Feature,
           FeatureVector, Model, ScoreProcessor,
           __name__, __version__, __author__,
           __author_email__, __description__, __url__]
