Revision Scoring
================
A generic, machine learning-based revision scoring system designed to be used
to automatically differentiate damage from productive contributory behavior on
Wikipedia.

Installation
================
In order to use this, you need to install a few packages first:

``pip install nltk nose deltas pytz mediawiki-utilities``

Examples
========

Feature extraction:
    
    .. code-block:: python
    
        >>> from mw.api import Session
        >>>
        >>> from revscores import APIExtractor
        >>> from revscores.feature_extractors import (bytes_changed, chars_added,
        ...                                           day_of_week_in_utc,
        ...                                           hour_of_day_in_utc, is_custom_comment,
        ...                                           user_age_in_seconds, user_is_anon,
        ...                                           user_is_bot)
        >>>
        >>> api_extractor = APIExtractor(Session("https://en.wikipedia.org/w/api.php"))
        >>>
        >>> extractors = [bytes_changed, chars_added, day_of_week_in_utc,
        ...               hour_of_day_in_utc, is_custom_comment, user_age_in_seconds,
        ...               user_is_anon, user_is_bot]
        >>>
        >>> features = api_extractor.extract(
        ...     624577024,
        ...     extractors
        ... )

        >>> for extractor, feature in zip(extractors, features):
        ...     print("{0}: {1}".format(extractor, feature))
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
