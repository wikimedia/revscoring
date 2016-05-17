|travis|_ |codecov|_

Revision Scoring
================
A generic, machine learning-based revision scoring system designed to be used
to automatically differentiate damage from productive contributory behavior on
Wikipedia.

Example
========

Using a scorer_model to score a revision::

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

You'll also need to install `enchant <https://enchant.org>`_ compatible
dictionaries of the languages you'd like to use.  We recommend the following:

* ``languages.arabic``: aspell-ar
* ``languages.dutch``: myspell-nl
* ``languages.english``: myspell-en-us myspell-en-gb myspell-en-au
* ``languages.estonian``: myspell-et
* ``languages.french``: myspell-fr
* ``languages.german``: myspell-de-at myspell-de-ch myspell-de-de
* ``languages.hebrew``: myspell-he
* ``languages.hungarian``: myspell-hu
* ``languages.indonesian``: aspell-id
* ``languages.italian``: myspell-it
* ``languages.persian``: myspell-fa
* ``languages.polish``: aspell-pl
* ``languages.portuguese``: myspell-pt
* ``languages.spanish``: myspell-es
* ``languages.swedish``: aspell-sv
* ``languages.russian``: myspell-ru
* ``languages.ukrainian``: myspell-uk
* ``languages.vietnamese``: hunspell-vi

Authors
=======
    Aaron Halfaker:
        * `http://halfaker.info`
    Helder:
        * `https://github.com/he7d3r`
    Adam Roses Wight:
        * `https://mediawiki.org/wiki/User:Adamw`
    Amir Sarabadani:
	* `https://github.com/Ladsgroup`

.. |travis| image:: https://api.travis-ci.org/wiki-ai/revscoring.png
.. _travis: https://travis-ci.org/wiki-ai/revscoring
.. |codecov| image:: https://codecov.io/github/wiki-ai/revscoring/revscoring.svg
.. _codecov: https://codecov.io/github/wiki-ai/revscoring
