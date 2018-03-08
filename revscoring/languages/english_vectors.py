from revscoring.datasources.meta import vectorizers

google_news_kvs = vectorizers.word2vec.load_kv(
    filename='GoogleNews-vectors-negative300.bin.gz', limit=150000)
