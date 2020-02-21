# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]

## [2.6.7]

### Fixed
* Reference to english idioms data file

## [2.6.6]

### Added
* English language idioms
* tag_str and template_str datasources in features.wikitext.revision

## [2.6.5]

### Added
* Support for native gensim vectors and mmaps

### Changed
* word2vec constructor is reverted back to old behavior for memory usage reasons

## [2.6.4]

### Changed
* word2vec is generalized and constructor now takes keyed_vectors

### Fixed
* Bumps gensim version to 3.8.1 to deal with smart_open warning

## [2.6.3]

### Fixed
- Fixes name of german language utils
- Rates are now properly formatted when labels are long or numerous
- word2vec generator now yields nothing rather than zero'd vectors when a word
  isn't found.

## [2.6.2]

### Added
- Adds explicit multi-dictionary support to English and German

### Fixed
- Minor fix to serbian badwords
- Add "sudo" to installation commands in readme
- Minor fix to English regexes


## [2.6.1]

### Fixed
- revscoring.Model.model_info now has metrics sorted in label-order

## [2.6.0]

### Added
- Added release automation to PyPI via TravisCI.
- Added CHANGELOG.md
- Added revscoring.languages.basque (Minimal dictionary support)
- Added <additional-field> to feature_csv utility.

## [2.5.2] - 2019-08-06

### Changed
Pin sklearn to 0.20.3

## [2.5.1] - 2019-07-29

### Changed
- Bumped more-itertools requirement to 7.2.x

## [2.5.0] - 2019-07-29

### Added
- Added a specific feature for reference claims in Wikibase sources.

### Changed
- Updated the versions of numpy,scipy & scikit-learn - @urstrulykkr

### Fixed
- No dupes in `trim()` function.
- Count ref statements instead of ref claims in Wikibase sources.
- Minor fix to setup.py for PyPI distribution.

## [2.4.0] - 2019-05-19

### Added
- Badwords, informals, and `words_to_watch` for Chinese.
- Pre-processing to regex matches so that we can have traditional Chinese converted to simplified.

### Changed
- Better error logging for `cv_train`.
- Updated language assets for Dutch.
- Added the part for running tests to README.
- Moved tests out of production code.
- Move pytest out of requirements.txt
- Upgrade travis image to xenial.
- Fixed order of imports / isort.

## [2.3.4] - 2019-02-07

### Changed
- Bumped yamlconf version to 0.2.4.
- Removed python 3.4 from travis build.

## [2.3.3] - 2019-02-06

### Fixed
- Turn members of dependents to string value.

## [2.3.2] - 2019-02-04

### Changed
- Use `sklearn.model_selection` instead of `sklearn.cross_validation`.
- Send `all_dependents` as a list, make it a set everywhere else.

### Fixed
- Properly set Datasource/Feature names for b/c aliases.

## [2.3.1] - 2019-01-30

### Changed
- Make basic datasources all json-serializable.

### Fixed
- Fix revscoring extract for users with 2FA.

## [2.3.0] - 2018-12-18

### Added
- Handling for schema issues for multilabel and "boolean".

## [2.2.7] - 2018-11-27

### Added
- Added Galician language assets.
- Added enwiki words to watch.

### Changed
- README: Fix apt-get command block

### Fixed
- Fixed meta feature naming for sum/max/etc.

## [2.2.6] - 2018-08-08

### Changed
- API changes to use the new MCR-aware params and format.
- Updated README.md formatting for language installs.
- Started using `mwbase` instead of `pywikibase` in wikibase-related datasources.
- usage string and API fixes

### Fixed
- Fixed score schema for ProbabilityClassifier.

## [2.2.5] - 2018-06-11

### Changed
- Handles 'nazism' as an english badword.

## [2.2.4] - 2018-06-04

### Changed
- Use `--labels` in tune.

### Fixed
-  revscoring.features.meta.aggregators handles numpy array.

## [2.2.3] - 2018-05-04

### Changed
- Word vectors - emit a null vector on empty string.

## [2.2.2] - 2018-04-16

### Changed
- Restricts numpy and scipy requirements to higher versions and sorts requirements.txt.
- Bumps scikit-learn's requirement to 0.19.x.

## [2.2.1] - 2018-04-16

### Added
- Added intersection utility.

### Changed
- Minor updates to spanish.py formatting.
- Use global vectors for better multiprocessing.
- Upgrade mwph to v0.5.x

### Fixed
- Fixed a bug in `load_kv` for Word2Vec.

### Removed
- Removed `english_vectors`.

## [2.2.0] - 2018-02-27

### Added
- Word2Vec features

### Changed
- Major refactoring to eliminate sklearn's native multilabel classification and introduce per label binary classification.
- List of sklearn's binary classifiers are stored in Revscoring's classifier wrapper, one for each label.
- Tests modified for multilabel.

## [2.1.0] - 2017-12-29

### Added
- Added Icelandic language support.
- Multilabel random forest.
- Added Catalan language assets.
- Fast scoring for fast cross validation.

### Changed
- Python 3 is now a hard requirement.
- Row formatting for long label names.
- Support for specifying label weights in multilabel classification.
- Use nltk stopwords library instead of homemade list wherever possible.

### Fixed
- Selectors: Count documents, labels per document instance, not per token.
- Fixed label type issue in label-config.

## [2.0.10] - 2017-11-08

### Changed
- Use pytest-cov to collect coverage.
- Ignore test-like functions using tox.ini

## [2.0.9] - 2017-10-06

### Changed
- Migrate from nosetests to pytests.
- Updated nltk download instructions to include additional corpora.
- Handle ModelInfo lookup error.

### Fixed
- Key pattern in `format_str` for ModelInfo.

## [2.0.8] - 2017-10-06

### Added
- Additional tests to filters and mappers.

### Changed
- Limit memory usage of threshold statistics.
- Use `__slots__` in ScaledClassificationMatrix to reduce memory usage.
- Added `threshold_ndigits` to classification params.

## [2.0.7] - 2017-09-22

### Added
- Added Serbian language assets.

### Changed
- Natively handle bz2 compressed model files.

## [2.0.6] - 2017-09-11

### Added
- Bosnian language assets.

### Changed
- Changes uk dict recommendation to aspell (from myspell).

### Fixed
- Fixed sorting in tune utility.

## [2.0.5] - 2017-09-01

### Changed
- Use tqdm (progress bar) in extract utility.

### Fixed
- Context manager to close model file after load.

### Removed
- Removes setuptools requirement.

## [2.0.4] - 2017-09-01

### Added
- Croatian language support.

### Changed
- Better handing of `label_weights` in Linear model.

### Fixed
- Fixed `tune` utility bug T174704.

## [2.0.3] - 2017-08-29

### Added
- Lativan language support

### Changed
- Implemented info paths in `model_info` utility.
- Adds label information to model_info "score_schema".
- Allow stats in ThresholdOptimization to include exclamation points.

### Fixed
- Fixed arg parsing issues in `model_info` utility.

## [2.0.2] - 2017-08-10

### Added
- Added documentation to ScaledThresholdStatistics test.
- Implemented access to thresholds. - @mdew192837

### Fixed
- Fixed model info formatting bug in `cv_train`.
- Fixed test for ScaledThresholdStatistics.
- Updated ScorerModel references in README. - @profgiuseppe
- Fixed `python setup.py upload_docs` call for pypi.

## [2.0.1] - 2017-08-03

### Added
- New utility `union_merge_observations`.

### Changed
- Included ModelInfo to docs and cleans up some references.
- Extends tests for `model_info` and `score_processor`.

### Fixed
- Fixed typo in module path.
- Fixed main languages documentation.

## [2.0.0] - 2017-07-13

### Added
- Added thresholds class.
- Added tests for threshold optimization.
- Added threshold optimizations to `cv_train` utility.
- Added logistic regression to basic model documentation.

### Changed
- Total overhaul of scorers and statistics.
- Updated `tune` utility to now uses new statistics.
- Centralized statistic pattern parsing.
- Moved `OrderedDict` to `_data` attr in `ModelInfo`.
- Moved to `model_info` pattern.

### Fixed
- Minor fix to utilites to fix tests.
- AUC metrics
- Fixed model's composition strategy.

### Removed
- Removed statistics schema.json

## [1.3.18] - 2017-07-17

### Changed
- Bumped requirement for mwtypes to include 0.3.x

## [1.3.17] - 2017-07-13

### Changed
- Disabled tamil dictionary.

## [1.3.16] - 2017-07-13

### Added
- Added Albanian language assets.

### Changed
- Tweak lol regexp + use same regexp for portuguese.py
- Disabled Bengali dictionary.

### Fixed
- Fixed typo in `BernoulliNB()`
- Put missing options where docopt can find them.

## [1.3.15] - 2017-06-25

### Changed
- Added mysqltsv to requirements.txt

### Fixed
- Fixed old reference to README.rst in setup.py.
- Fixed pathological backtracking regexp

## [1.3.14] - 2017-06-16

### Added
- Added ascii transliterations to Tamil badwords.
- Added `CODE_OF_CONDUCT.md`

### Changed
- Bumped pytz requirement to 2017.2
- Convert README from rst to .md
- Included another German badword.
- Use trusty image for travis build.
- Minor fix to `extractors.regex` so that it can handle backwards compatibility.

## [1.3.13] - 2017-06-05

### Fixed
- Minor fixes to regex exclusions.

## [1.3.12] - 2017-06-05

### Added
- Greek language assets.

### Changed
- Regex exclusion strategy for RegexMatches.

## [1.3.11] - 2017-05-20

### Added
- Added Bengali language assets.
- Implemented Flesch readability complexity.

### Changed
- Bumped deltas to 0.4.6
- included bash-command for language install

### Fixed
- Fixed issue caused by old deltas library

## [1.3.10] - 2017-03-28

### Added
- Korean language assets and tests.

### Fixed
- Fixed naming issues with datasources.meta.filters
- Fixed lower() to work for Turkish chars.

## [1.3.9] - 2017-03-18

### Added
- Adds datasources.meta.mappers.derepeat token processor.
- Adds datasources.meta.mappers.de1337 token processor.

### Changed
- Bumped deltas requirement to 0.4.5.

### Fixed
- Test for gramming.

## [1.3.8] - 2017-03-10

### Changed
- Included tests for finnish

### Removed
- Finnish dict dependency.

## [1.3.7] - 2017-03-10

### Added
- Finnish language assets

### Changed
- Extends Estonian language assets.

## [1.3.6] - 2017-01-31

### Changed
- Added worker count param to `cv_train`.
- Better link for enchant docs.

### Fixed
- Fix broken link in README

## [1.3.5] - 2017-01-27

### Added
- Added Romanian language assets.

## [1.3.4] - 2017-01-11

### Added
- Added about.py file for tracking metadata.

### Fixed
- Fixes `rev_doc` injection bug in `api.Extractor`.

## [1.3.3] - 2017-01-05

### Added
-  Added `fetch_text` utility.

### Changed
- Added shuffling to cross-validation.
- Updated revscoring.py docstrings to be consistent.

## [1.3.2] - 2016-11-29

### Added
- Added basic sentence datasources.

### Changed
- Normalize NaN, Inf, and -Inf in JSON formatting.
- Bumped deltas requirement to 0.4.x

### Removed
- Removed `demo_load_model` script.

## [1.3.1] - 2016-11-03

### Added
- Cross-validation support for models.
- Added `recall_at_precision` metric.

### Fixed
- Minor fixes to tune utility
- Fixes `recall_at_fpr` metric.

## [1.3.0] - 2016-09-02

### Added
- Added `FeatureVector` class.
- Added `vectorizers.vectorize()` method.
- Added term frequency gramming, hashing and selection.

### Changed
- Updated `SklearnClassifier` to handle `FeatureVector`.
- Moved `extract_features` to `extract` (a more general name).
- Generalized feature extraction pattern.
- Included Cache & JSON style for utilities.

## [1.2.9] - 2016-08-09

### Added
- OSX install instructions in README.
- Tamil language utilities

### Changed
- Updated hashing vectorizer example with a `feature_importance` histogram.

### Fixed
- README usage updated to reflect renamed extractor.

## [1.2.8] - 2016-07-08

### Added
-  Tests for API extractor datasources.

### Fixed
- Minor cache preservation issue in `dependencies.solve()`.

## [1.2.7] - 2016-06-30

### Added
- Czech language assets
- Norwegian language utilities

### Changed
- Prepend local dir on path for all utilities that use classpaths.

### Fixed
- Minor fix to OfflineExtractor's use of caches.

## [1.2.6] - 2016-05-19

### Fixed
- Initialize caches in extractor.

## [1.2.5] - 2016-05-18

### Added
- Swedish language utilities.

### Changed
- Improved performance on Persian regexes.

### Fixed
-  Fixed test for `time_since_registration` for anons.

## [1.2.4] - 2016-05-10

### Changed
- Improved English badwords regexs.
- Intermediate filtered stage for mwparserfromhell wikicode.
- Makes cache preserve through `extractor.extract()` and `context.solve()`

## [1.2.3] - 2016-04-30

### Changed
- Speeded up dictionary features by ~2

## [1.2.2] - 2016-04-27

### Added
- `cpu` and `IO` config for ScoreProcessor & score utility.
- Added Hungarian language support.

### Changed
- Cleaned verbose of `feature_extractor` for deleted stuff

## [1.2.1] - 2016-04-12

### Changed
- Made score utility faster.

###Fixed
- Fixed extractor error.

## [1.2.0] - 2016-04-12

### Added
- Added the possibility to log in to the feature extractor.
- Implemented feature profiling
- Added Russian language utility.
- Added hashing vectorizer example notebook.
- Language assets for Hindi.

### Changed
- Updated regexes to match new tests.

### Fixed
- Missing commas and additional entries for English language tests.
- Updated LICENSE due to a mistake from an old copy-paste.
- Minor fix to docs for regex matcher

## [1.1.8] - 2016-03-28

### Fixed
- Fixed feature extraction for page creation revisions.

## [1.1.7] - 2016-03-27

### Changed
- Added a basic test for `solve()`.
- Extends scipy requirement back to 0.13.3

### Fixed
- Minor fixes to `regex_matches` feature names.

## [1.1.6] - 2016-03-26

### Added
- Japanese language support.

### Changed
- Modifications to regex extraction to not use word boundary chars sometimes.

### Fixed
- Fixed cache usage in extraction.

## [1.1.5] - 2016-03-21

### Fixed
- yamlconf requirement range error.

## [1.1.4] - 2016-03-21

### Changed
- Bumped yamlconf requirement to > 0.1.0

## [1.1.3] - 2016-03-15

### Changed
- Changes `cache` argument to `caches` in api.Extractor.
- Added Amir to README.

## [1.1.2] - 2016-03-15
### Changed
- Handling of revision caches to API extractor.

## [1.1.1] - 2016-03-13

### Fixed
- Fixed minor issue making f1 test statistic unavailable.

## [1.1.0] - 2016-03-13

### Added
- F1 test statistic generator.

## [1.0.3] - 2016-03-10

### Removed
- Random print to stdout in `scorer_models.util`.

## [1.0.2] - 2016-03-10

### Added
- Added tests for model utilities.

### Changed
- Added `balanced_sample` option to all scorer models.

### Fixed
- Typo in Feature Engineering notebook.
- 'NoneType' has no len() when processing `longest_repeated_char`.

## [1.0.1] - 2016-03-06
First official 1.x release!

### Added
- Added proportional features to wikibase.
- Basic `revision_oriented` features implemented and tested.
- Added `GradientBoosting` scorer model
- Added Polish language support and tests.
- Added Arabic language support.
- Added `DependentSet` to dependencies.
- Added documentation for languages.

### Changed
- Updated IPython notebooks.
- Fixed documentation around test statistics and base `revision_oriented` features.
- Included "sup" to informals for English features.
- Handled `CaughtDependencyError` error.
- Added `ref_tags` to `wikitext.revision`.
- Bumped pywikibase requirement to 0.0.4
- Updated documentation for features.
- Applied new API Extractor to utilities.
- Improved test coverage
- Minor generalization to hebrew's test cases for older dictionaries.
- Fixed typo in wikibase tests. alan (touring --> turing)
- Refactored entire feature structure.
- Added pywikibase to requirements.
- Moved tokenized.delta to tokenized.diff.
- User.name --> User.text
- Moved basic regex operations.
- Added token frequencies to datasources/meta.
- Persian badwords explained.
- Added `revision.diff` to datasources.
- `revision_oriented` uses `DependentSet` now.
- Improved Documentation.

### Fixed
- Fixed a minor bug in accuracy calculation when using scaling or centering in a scorer model.

### Removed
- Removed backtracking requirements from english badwords and informals. Increased performance X3
- Removed old backwards compatible ...Model classes from `scorer_models`

## [0.7.11] - 2015-12-14

### Changed
- Tests for more Portuguese badwords
- Switched to using the `average_precision` scorer when `pr_auc` is required.
- Removes 'ha' from italian informals and add test to be sure.

## [0.7.10] - 2015-12-13

### Fixed
- Fixed issues in offline extractor.

## [0.7.9] - 2015-12-13

### Changed
- Adds `pr_auc_score` to metrics available for tuning.
- Improved comments and added variations for a few Portuguese bad words.
- Adds yamlconf to requirements.txt
- Added `OfflineExtractor` to extractors.

### Removed
- Section about "changelog" vs "CHANGELOG".

## [0.7.8] - 2015-12-07

### Changed
- Fixed logging and table formatting in `tune` utility.

## [0.7.7] - 2015-12-06

### Fixed
- Fixed merge issue in `tune` utility.

## [0.7.6] - 2015-12-06

### Changed
- Adds `cv-timeout` option to tune utility.

## [0.7.5] - 2015-12-06

### Changed
- Updated revscoring utility to list `model_info` and tune utilities.
- Added error handling to cross-validation.
- Updated README w/ badges and source highlighting.

### Fixed
- Removed `import_from_path` issue in `extract_features` utility.
- Fixed test for sklearn classifier.

## [0.7.4] - 2015-12-01

### Fixed
- Minor fix in Bernoulli spelling.
- Fixed minor issue in svc params config.
- Minor fixes to tuning.

### Changed
- Switched tuning utility to use multiprocessing directly.
- Cleanup to tuning utility and add config files for each classifier's param space.

### Removed
- Removed old config ptwiki config files that were never used.

## [0.7.3] - 2015-11-22

### Added
- Added estonian and ukrainian languages

### Changed
- Switches to aspell packages for et and uk in travis
- Replaces duplicate myspell-de-ch with myspell-de-de in README.rst

### Fixed
- TravisCI errors

## [0.7.2] - 2015-11-07

### Fixed
- Fixed binary operators.

## [0.7.1] - 2015-11-07

### Changed
- Added `and/or/not` operators to features

### Fixed
- Fixes enchant link in README.rst

## [0.7.0] - 2015-11-01

### Added
- Adds `--test-prop` param to `train_test` utility.
- Adds a Dockerfile for building an image that will run an ipython notebook to build a revscoring project.
- Adds a `trim()` function for reducing a `feature_list` to it's basic 'features' -- a prerequisite for wikimedia/ores#100
- Adds basic language features for Dutch, German and Italian.

### Changed
- Widens version requirements for scipy and numpy to make compiling dependencies from source less common.
- Substantial improvements to documentation. Now using 'alabaster' theme and simplified examples.

## [0.6.4] - 2015-10-03
Since 0.5.0:

### Added
- Adds batching to Feature extraction for more speed.
- Adds wheel support
- Adds `model_info` storage & utility

### Changed
- Improved error reporting in api extractor
- Change to configuration -- APIExtractor now requires host instead of url
- Silences a utf16 encoding warning in enchant

### Fixed
- Fixes an issue with looking up user info in APIExtractor
- Fix travis builds, add coverage to reports

### Removed
- Drops `mediawiki-utilities` in favor of `mwapi` and `mwtypes`

## [0.5.0] - 2015-09-05

This release represents a major backwards incompatibility

### Added
- Languages as feature sets.

### Changed
- Codebase is now PEP8 compliant.

## [0.4.10] - 2015-08-08

### Fixed
- APIExtractor can't find language utilities

## [0.4.9] - 2015-08-05

### Changed
- Extended badwords and adds informal words for Persian language

### Fixed
- Fixes pickling issue with languages (see #159)

## [0.4.8] - 2015-08-04

### Changed
- Synchronizes dependency versions with https://github.com/wiki-ai/ores and generalizes both.

## [0.4.6] - 2015-08-04

### Changed
- Improved installation instructions
- Selective language imports (no need to download all the dictionaries anymore)

### Fixed
- Math domain error when processing imported revisions (`user.age`).
- Handle `RevisionDocumentNotFound` when scoring new pages

## [0.4.5] - 2015-07-26

### Added
- Adds Vietnamese support

### Fixed
- Feature `user.is_bot` errors out with None 'groups'.

## [0.4.4] - 2015-07-17

### Added
- Adds spanish language utilities
- Adds informal words utility to English and Spanish languages

### Changed
- Converts English language badwords detection to regex based strategy.

## [0.4.1] - 2015-07-16

### Added
- Adds 'indonesian' language (thanks @kenrick95!)

### Changed
- Added `balance_labels` arg to constructor of SVC models.
- Improves formatting of `train_test` results (and implements one vs. rest ROC for multiclass models)

## [0.4.0] - 2015-06-09

### Changed
- Move "scorer" out of the library (and into ORES).
- Completed documentation (see http://pythonhosted.org/revscoring)
- Implemented a refactoring for the 'dependencies'.
- Also implements some new functions list dig() and expand()

## [0.3.1] - 2015-06-06

### Changed
- Specify version of scipy same as in Ubuntu Trusty

## [0.3.0] - 2015-05-26

### Added
- New `Features` and `Datasources`.

### Changed
- Better performance.
- Test completeness.
- Batch feature extraction

## [0.2.0] - 2015-04-03

### Fixed
- Fix bug where `max()` arg is an empty sequence.

## [0.1.0] - 2015-02-14

### Added
- Added minimal implementation of Turkish language

### Changed
- Improved behavior of MLScorer and MLScorer model.
- Improved README.

## [0.0.3] - 2015-02-01
This is an early release of the revscoring library.

### Added
- Added revscoring.datasources (Datasource, 20 implemented)
- Added revscoring.extractors (APIExtractor)
- Added revscoring.features (Feature, 42 implemented)
- Added revscoring.languages (english & portuguese)
- Added revscoring.scorers (MLScorer/MLScorerModel, SVCModel, LinearSVCModel & RBFSVCModel)
- Added revscoring.dependent (Dependent, Solve)
- Tests for all new modules.

## [0.0.2] - 2014-07-10
### Added
- Explanation of the recommended reverse chronological release ordering.

## [0.0.1] - 2014-05-31
### Added
- Basic project setup.
