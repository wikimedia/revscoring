Revision Scoring
================
A generic, machine learning-based revision scoring system designed to be used
to automatically differentiate damage from productive contributory behavior on
Wikipedia.

Examples
========

Scoring models:

    .. code-block:: python

        >>> from mw.api import Session
        >>>
        >>> from revscoring.extractors import APIExtractor
        >>> from revscoring.languages import english
        >>> from revscoring.scorers import MLScorerModel
        >>>
        >>> api_session = Session("https://en.wikipedia.org/w/api.php")
        Sending requests with default User-Agent.  Set 'user_agent' on api.Session to quiet this message.
        >>> extractor = APIExtractor(api_session, english)
        >>>
        >>> filename = "models/reverts.halfak_mix.trained.model"
        >>> model = MLScorerModel.load(open(filename, 'rb'))
        >>>
        >>> rev_ids = [105, 642215410, 638307884]
        >>> feature_values = [extractor.extract(id, model.features) for id in rev_ids]

        >>> scores = model.score(feature_values, probabilities=True)
        >>> for rev_id, score in zip(rev_ids, scores):
        ...     print("{0}: {1}".format(rev_id, score))
        ...
        105: {'probabilities': array([ 0.96441465,  0.03558535]), 'prediction': False}
        642215410: {'probabilities': array([ 0.75884553,  0.24115447]), 'prediction': True}
        638307884: {'probabilities': array([ 0.98441738,  0.01558262]), 'prediction': False}

Feature extraction:

    .. code-block:: python

        >>> from mw.api import Session
        >>>
        >>> from revscoring.extractors import APIExtractor
        >>> from revscoring.features import diff, parent_revision, revision, user
        >>>
        >>> api_extractor = APIExtractor(Session("https://en.wikipedia.org/w/api.php"))
        Sending requests with default User-Agent.  Set 'user_agent' on api.Session to quiet this message.
        >>>
        >>> features = [revision.day_of_week,
        ...             revision.hour_of_day,
        ...             revision.has_custom_comment,
        ...             parent_revision.bytes_changed,
        ...             diff.chars_added,
        ...             user.age,
        ...             user.is_anon,
        ...             user.is_bot]
        >>>
        >>> values = api_extractor.extract(
        ...     624577024,
        ...     features
        ... )
        >>> for feature, value in zip(features, values):
        ...     print("{0}: {1}".format(feature, value))
        ...
        <revision.day_of_week>: 6
        <revision.hour_of_day>: 19
        <revision.has_custom_comment>: True
        <(revision.bytes - parent_revision.bytes_changed)>: 3
        <diff.chars_added>: 8
        <user.age>: 71821407
        <user.is_anon>: False
        <user.is_bot>: False


Installation
================
In order to use this, you need to install a few packages first:

``pip install revscoring``

You'll need to download NLTK data in order to make use of language features.

.. code-block:: python

    >>> python
    >>> import nltk
    >>> nltk.download()
    >>> Downloader> d
    >>> Identifier> wordnet
    >>> Downloader> d
    >>> Identifier> omw
    >>> Downloader> d
    >>> Identifier> stopwords
    >>> Downloader> q
    >>> exit()


You might need to install some other dependencies depending on your operating
system.  These are for ``scipy`` and ``numpy``.

Linux Mint 17.1:

1. ``sudo apt-get install g++ gfortran liblapack-dev python3-dev myspell-pt myspell-fa myspell-en-au myspell-en-gb myspell-en-us myspell-en-za  myspell-fr``

Ubuntu 14.04:

1. ``sudo apt-get install g++ gfortran liblapack-dev libopenblas-dev python3-dev myspell-pt myspell-fa myspell-en-au  myspell-en-gb myspell-en-us myspell-en-za myspell-fr``

Authors
=======
    Aaron Halfaker:
        * `http://halfaker.info`
    Helder:
        * `https://github.com/he7d3r`
