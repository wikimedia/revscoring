Wednesday, Sept. 10th, 2014
===========================
I flattened things.  I think this is nicer.

* revscores
    * datasources
    * feature_extractors
    * model
        * ???
    * util
        * dependencies

So now... I need to figure out what's up with models.

Option 1:
---------
* Each model is a class
* An instance must be train()'d and should be test()'d
* A trained instance can predict()

Pros:

    * I've built this class structure before for wikiclass and it went Okay

Cons:

    * Are we going to accept anything other than classifiers?

Option 2:
---------
* Abstract away from model to build a Scorer
* An instance of a scorer can be train()'d and test()'d,
  but it doesn't need to be.
* A scorer instance can score()

Pros:

    * This will increase flexibility for non-machine learning scorers
      (e.g. Huggle)
    * This project *is* called 'revscores'

Cons:

    * More abstraction.  

Monday, Sept. 8th, 2014
=======================

Right now, you need to import from `revscores.features.features`.  That's dumb. I could rename the higher-level `features` to `feature_extraction`.  That's a little verbose.  Then you'd import from `revscores.feature_extraction.features` -- which doesn't sound as dumb, but is verbose.

* revscores
    * feature_extraction
        * features
        * datasources
        * extractor
        * dependencies
    * models
        * ???
