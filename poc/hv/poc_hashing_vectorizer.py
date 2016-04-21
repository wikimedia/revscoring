import csv
import pprint
import random
import mwapi
import mwparserfromhell as mwparser
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import HashingVectorizer
pp = pprint.PrettyPrinter(indent=4)

def get_pageid(doc):
    pageid = doc['query']['pages'].keys()
    pageid = list(pageid)[0]
    return pageid

def get_parent_revid(doc):
    parent_revid = doc['query']['pages'][str(get_pageid(doc))]['revisions'][0]['parentid']
    return parent_revid

def get_contents(revid):
    """
    get content for revid and it's parent
    /w/api.php?action=query&format=json&prop=revisions&pageids=5887233&rvprop=ids%7Ccontent&rvlimit=2&rvstartid=655710468
    """

    session = mwapi.Session("https://en.wikipedia.org",
                            user_agent="Hashing vectorizer P.O.C <ruj.sabya@gmail.com>, <aaron.halfaker@gmail.com>")

    doc = session.get(action="query", prop="revisions", revids=[revid], rvprop=['ids'])
    pageid = get_pageid(doc)
    parent_revid = get_parent_revid(doc)
    doc = session.get(action="query", prop="revisions", pageids=[pageid], rvprop=['ids', 'content'], rvlimit=2, rvstartid=[revid])

    # todo - how do we know which is parent and which is current? is it ordered like I assumed?
    current_text = doc['query']['pages'][str(pageid)]['revisions'][0]['*']
    parent_text = doc['query']['pages'][str(pageid)]['revisions'][1]['*']

    result = {'parent': parent_text, 'current': current_text}
    return result

    # with open("parent.txt", "w") as text_file:
    #     print(parent_text, file=text_file)
    #
    # with open("current.txt", "w") as text_file:
    #     print(current_text, file=text_file)

#contents = get_contents(623818349)

def read_tsv(filename):
    observations = []
    with open(filename,'rt') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            contents = get_contents(row[0])
            observations.append((contents['current'], contents['parent'], row[-1]))
            #pp.pprint(observations)
            if len(observations) >= 6:
                break
    return observations

def extract_features():
    filename = 'enwiki.features_damaging.20k_2015.tsv'
    filename = 'first50.tsv'
    observations = read_tsv(filename)

    train_set = observations[:int(len(observations)*0.8)]
    test_set = observations[int(len(observations)*0.8):]

    print(len(observations))

    hv = HashingVectorizer(n_features=2*20)
    texts_current_revid, texts_parent_revid, labels_y = zip(*train_set)
    features_X_current = hv.transform(texts_current_revid)
    features_X_parent = hv.transform(texts_parent_revid)
    features_X_diff = features_X_current - features_X_parent

    return features_X_diff, labels_y

features, labels = extract_features()
gbc = GradientBoostingClassifier()
labels = (True, False, True, False) #TODO - faked for at least getting two classes
gbc.fit(features, labels,
            sample_weight=[18967 / (798 + 18967) if l == True else 798 / (798 + 18967) for l in labels])

print("Done")
# True (damaging): 798, False (not damaging): 18967, Total: 19765