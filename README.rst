Revision Scoring
================
A generic, machine learning-based revision scoring system designed to be used
to automatically differentiate damage from productive contributory behavior on
Wikipedia.

Examples
========


Feature extraction:
    
    .. code-block:: python
    
            >>> from mw.api import Session
            >>>
            >>> from revscores.features import Extractor
            >>> from revscores.features.features import (bytes_changed, is_anon, is_mainspace,
            ...                                          is_same_author, is_section_comment,
            ...                                          num_words_added, num_words_removed)
            >>>
            >>> extractor = Extractor(Session("https://en.wikipedia.org/w/api.php"), {})
            >>>
            >>> feature_values = extractor.extract(
            ...     624577024,
            ...     [is_section_comment, is_anon, is_mainspace, bytes_changed, is_same_author,
            ...      num_words_added, num_words_removed]
            ... )
            >>> print(feature_values)
            [True, False, True, -3, False, 2, 0]

Authors
=======
    Aaron Halfaker:
        * `http://halfaker.info`
