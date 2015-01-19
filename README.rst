Revision Scoring
================
A generic, machine learning-based revision scoring system designed to be used
to automatically differentiate damage from productive contributory behavior on
Wikipedia.

Installation
================
In order to use this, you need to install a few packages first:

``pip install -r requirements.txt``

You'll need to download NLTK data in order to make use of language features.

.. code-block:: python

    >>> python
    >>> import nltk
    >>> nltk.download()
    >>> Downloader> d
    >>> Identifier> wordnet
    >>> Downloader> d
    >>> Identifier> omw
    >>> Downloader> q
    >>> exit()


You might need to install some other dependencies depending on your operating
system.

Linux Mint 17:

1. ``sudo apt-get install g++ git python-sklearn python3.4-dev libatlas-base-dev gfortran``

Ubuntu 14.04:

1. ``sudo apt-get install python3-dev gfortran libopenblas-dev liblapack-dev''`

Examples
========

Feature extraction:
    
    .. code-block:: python
    
        >>> from mw.api import Session
        >>>
        >>> from revscores.extractors import APIExtractor
        >>> from revscores.features import (bytes_changed, chars_added,
        ...                                           day_of_week_in_utc,
        ...                                           hour_of_day_in_utc, is_custom_comment,
        ...                                           user_age_in_seconds, user_is_anon,
        ...                                           user_is_bot)
        >>>
        >>> api_extractor = APIExtractor(Session("https://en.wikipedia.org/w/api.php"))
        >>>
        >>> features = [bytes_changed, chars_added, day_of_week_in_utc,
        ...               hour_of_day_in_utc, is_custom_comment, user_age_in_seconds,
        ...               user_is_anon, user_is_bot]
        >>>
        >>> values = api_extractor.extract(
        ...     624577024,
        ...     features
        ... )
        >>> for feature, value in zip(features, values):
        ...     print("{0}: {1}".format(feature, value))
        ...
        <bytes_changed>: 3
        <chars_added>: 8
        <day_of_week_in_utc>: 6
        <hour_of_day_in_utc>: 19
        <is_custom_comment>: True
        <user_age_in_seconds>: 71821407
        <user_is_anon>: False
        <user_is_bot>: False


Authors
=======
    Aaron Halfaker:
        * `http://halfaker.info`
    Helder:
        * `https://github.com/he7d3r`
