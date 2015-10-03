"""
`revscoring` is a generic, revision scoring system designed to be used to
automatically "score" revisions in a MediaWiki installation.  This library
eases the construction and use of Machine Learning model-based scoring
strategies.

* See the :ref:`API reference <api-reference>` for detailed information

Key Features
------------

Scorer Models:
    :class:`~revscoring.scorer_models.scorer_model.ScorerModel` are the core of
    the `revscoring` system.  Provide a simple interface with complex
    internals.  Most commonly, :class:`~revscoring.scorer_models.MLScorerModel`
    (Machine Learned) is
    :meth:`~revscoring.scorer_models.MLScorerModel.train`'d and
    :meth:`~revscoring.scorer_models.MLScorerModel.test`'d on
    labeled data to provide a basis for scoring.
    We currently support: :mod:`~revscoring.scorer_models.svc`,
    :mod:`~revscoring.scorer_models.rf` and :mod:`~revscoring.scorer_models.nb`
    type models. (see :mod:`revscoring.scorer_models`)

    Example: *TODO*

Feature extraction:
    Revscoring provides a dependency-injection-based feature extraction
    framework that allows new features to be built on top of old.  This allows
    a powerful means to expressing new features and a simple way to address
    efficiency concerns. (see :mod:`revscoring.features`,
    :mod:`revscoring.datasources`, and :mod:`revscoring.extractors`)

    Example: *TODO*

Language support:
    Many features require language specific utilities to be available to
    support feature extraction.  In order to support this, we provide a
    collection of language utilities that integrate with our feature
    extraction system so as to be requested when necessary.  We support
    language utilities for the following languages:
    :data:`~revscoring.languages.english`,
    :data:`~revscoring.languages.french`,
    :data:`~revscoring.languages.hebrew`,
    :data:`~revscoring.languages.indonesian`,
    :data:`~revscoring.languages.persian`,
    :data:`~revscoring.languages.portuguese`,
    :data:`~revscoring.languages.spanish`,
    :data:`~revscoring.languages.turkish`, and
    :data:`~revscoring.languages.vietnamese`.
    (see :mod:`revscoring.languages`)

    Example: *TODO*
"""
__version__ = "0.6.4"
