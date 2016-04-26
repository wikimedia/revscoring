# head -n 16000 enwiki.features_damaging.20k_2015.tsv > train.tsv
# tail -n 3765 enwiki.features_damaging.20k_2015.tsv > test.tsv
import csv
import pickle
import pprint
import random
import mwapi
import time
import sys
import mwparserfromhell as mwparser
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import HashingVectorizer
import sqlite3
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

    session = mwapi.Session('https://en.wikipedia.org',
                            user_agent='Hashing vectorizer P.O.C <ruj.sabya@gmail.com>, <aaron.halfaker@gmail.com>')

    try:
        doc = session.get(action='query', prop='revisions', revids=[revid], rvprop=['ids'])
    except:
        print("Error: ", sys.exc_info()[0])
        return False

    if 'badrevids' in doc['query']:
        # if the page related to the revision is deleted
        print ("bad revid: %s" % (revid))
        return False

    pageid = get_pageid(doc)
    parent_revid = get_parent_revid(doc)


    try:
        doc = session.get(action='query',
                          prop='revisions',
                          pageids=[pageid],
                          rvprop=['ids', 'content'],
                          rvlimit=2,
                          rvstartid=[revid],
                          rvdir='older')
    except:
        print("Error: ", sys.exc_info()[0])
        return False

    pp.pprint((pageid, revid))
    # todo - how do we know which is parent and which is current? is it ordered like I assumed?
    current_text = doc['query']['pages'][str(pageid)]['revisions'][0]['*']
    parent_text = doc['query']['pages'][str(pageid)]['revisions'][1]['*'] if parent_revid else ''

    result = {'revid':revid,
              'revid_parent': parent_revid,
              'parent': parent_text,
              'current': current_text}

    return result

def read_tsv(fileobj):
    tsvin = csv.reader(fileobj, delimiter='\t')
    for row in tsvin:
        yield row

def extract_features():
    hv = HashingVectorizer(n_features=2 ** 20)
    filename = 'train.tsv'

    f = open(filename,'rt')

    for observation in read_tsv(f):
        texts, label = zip(observation)
        text_current = texts[0]['current']
        features_current = hv.transform(
            (texts[0]['current'],
             texts[0]['parent']))
        features_parent = hv.transform((texts[0]['parent'],))
        features_diff = features_current - features_parent
        print(features_diff, label)
        break
    a = 3

def open_db():
    #sqllite
    conn = sqlite3.connect('data.db')
    return conn

def create_sqlite_tables():
    conn = open_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS observations
    (revid INTEGER PRIMARY KEY, other_features TEXT, is_damaging INTEGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS content
    (revid INTEGER PRIMARY KEY, revid_parent INTEGER, content_current BLOB, content_parent BLOB)''')

    conn.close()


def export_tsv_to_sqlite():
    create_sqlite_tables()
    conn = open_db()
    c = conn.cursor()

    filename = 'enwiki.features_damaging.20k_2015.tsv'
    f = open(filename,'rt')

    i = 1
    for row in read_tsv(f):
        print(i)
        i = i + 1
        other_features = pickle.dumps(row[1:-1])
        c.execute('''insert into observations
        (revid, other_features, is_damaging)
        values (?, ?, ?)''', (row[0], other_features, row[-1]))
    conn.commit()


    conn.close()

def read_db():
    conn = open_db()
    c = conn.cursor()

    # read from sqlite
    ret = c.execute('''select * from observations''')
    for row in ret:
        features = pickle.loads(row)
        pp.pprint(len(features))
        break


def download_conents():
    create_sqlite_tables()
    conn = open_db()
    c = conn.cursor()

    # read from sqlite
    ret = c.execute('''select revid from observations where revid not in (select revid from content)''')
    i = 1

    ci = conn.cursor()
    conn.isolation_level = None;
    for row in ret:
        revid = row[0]
        print(i, revid)
        i = i + 1
        content = get_contents(revid)

        if content == False:
            continue

        ci.execute('''INSERT INTO
          content(revid, revid_parent, content_current, content_parent)
          values (?, ?, ?, ?)''',
                        (content['revid'],
                         content['revid_parent'],
                         content['current'],
                         content['parent']
                        ))

# export_tsv_to_sqlite()
# read_db()
download_conents()


###

# extract_features()

#
# gbc = GradientBoostingClassifier()
#
# #labels = (True, False, True, False) #TODO - faked for at least getting two classes
# # True (damaging): 798, False (not damaging): 18967, Total: 19765
# gbc.fit(features, labels,
#             sample_weight=[18967 / (798 + 18967) if l == True else 798 / (798 + 18967) for l in labels])

print("Done")
