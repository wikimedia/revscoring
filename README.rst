Revision Scoring
================
A generic, machine learning-based revision scoring system designed to be used
to automatically differentiate damage from productive contributory behavior on
Wikipedia.

Examples
========

Using a scorer_model to score a revision:

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
    {'prediction': True, 'probability': {False: 0.4694409344514984, True: 0.5305590655485017}}


Installation
============
The easiest way to install `revscoring` is via the Python package installer
(pip).

``pip install revscoring``

You may find that some of `revscorings` dependencies fail to compile (namely
`scipy`, `numpy` and `sklearn`).  In that case, you'll need to install some
dependencies in your operating system.

Ubuntu & Debian:
  Run ``sudo apt-get install python3-dev g++ gfortran liblapack-dev libopenblas-dev``
Windows:
  'TODO'
MacOS:
  'TODO'

Finally, in order to make use of language features, you'll need to download
some NLTK data.  The following command will get the necessary corpus.

``python -m nltk.downloader stopwords``

You'll also need to install [enchant](https://enchant.org) compatible
dictionaries of the languages you'd like to use.  We recommend the following:

* ``languages.english``:  myspell-en-us myspell-en-gb myspell-en-au
* ``languages.french``: myspell-fr
* ``languages.spanish``: myspell-es
* ``languages.vietnamese``: hunspell-vi
* ``languages.hebrew``: myspell-he
* ``languages.portugueses``: myspell-pt
* ``languages.persian``: myspell-fa

Authors
=======
    Aaron Halfaker:
        * `http://halfaker.info`
    Helder:
        * `https://github.com/he7d3r`
    Adam Roses Wight:
        * `https://mediawiki.org/wiki/User:Adamw`
