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
from scipy.sparse import coo_matrix, vstack, hstack
from sklearn.externals import joblib
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score

import sqlite3
pp = pprint.PrettyPrinter(indent=4)

def fix_data_type(i):
    if i == 'True':
        return True
    if i == 'False':
        return False
    if i.isdigit() == True:
        return int(i)
    else:
        return float(i)
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
    print("Pageid, parent revid = ", (pageid, parent_revid))

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

def open_db(db_name = 'data.db'):
    conn = sqlite3.connect(db_name)
    conn.isolation_level = None;
    return conn

def create_sqlite_tables():
    # source db
    conn = open_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS observations
    (revid INTEGER PRIMARY KEY, other_features TEXT, is_damaging INTEGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS content
    (revid INTEGER PRIMARY KEY, revid_parent INTEGER, content_current BLOB, content_parent BLOB)''')

    conn.close()

    # features db
    conn = open_db('features.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feature_vector
    (revid INTEGER PRIMARY KEY, current BLOB, parent BLOB, diff BLOB, other_features BLOB, is_damaging INTEGER)''')
    conn.close()

    # score db
    # TODO - verify if we are populating other_features if features.db
    # is newly being created
    conn = open_db('score.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS score
    (revid INTEGER PRIMARY KEY, is_damaging_actual INTEGER, is_damaging_prediction INTEGER, score_positive REAL)''')
    conn.close()

def copy_other_features_to_features_db():
    conn_source = open_db();
    conn_features = open_db('features.db')
    cs = conn_source.cursor()
    cf = conn_features.cursor()

    ret = cs.execute('''SELECT revid, other_features FROM observations''')
    print('hi')
    for row in ret:
        print("inserting other features for", (row[0]))
        #other_features = pickle.loads(row[1])
        ret = cf.execute('''UPDATE feature_vector SET other_features=? WHERE revid = ?''',(row[1], row[0]))

    conn_source.close()
    conn_features.close()

    return

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
        c.execute('''INSERT INTO observations
        (revid, other_features, is_damaging)
        VALUES (?, ?, ?)''', (row[0], other_features, row[-1]))
    conn.commit()
    conn.close()

def download_conents():
    create_sqlite_tables()
    conn = open_db()
    c = conn.cursor()

    # read from sqlite
    ret = c.execute('''SELECT revid FROM observations WHERE revid NOT IN (SELECT revid FROM content)''')
    i = 1

    ci = conn.cursor()
    for row in ret:
        revid = row[0]
        print(i, revid)
        i = i + 1
        content = get_contents(revid)

        if content == False:
            ci.execute('''INSERT INTO content(revid) VALUES (?)''', (revid,))
            continue

        ci.execute('''INSERT INTO
          content(revid, revid_parent, content_current, content_parent)
          VALUES (?, ?, ?, ?)''',
                        (content['revid'],
                         content['revid_parent'],
                         content['current'],
                         content['parent']
                        ))

    conn.close()

def extract_features():
    hv = HashingVectorizer(n_features=2 ** 20, ngram_range=(1, 3))
    conn_source = open_db();
    conn_features = open_db('features.db')

    cs = conn_source.cursor()
    cf = conn_features.cursor()

    ret = cs.execute('''SELECT
     content.revid, content_current, content_parent, other_features, is_damaging
    FROM
     content INNER JOIN observations ON content.revid=observations.revid
    WHERE content.revid_parent IS NOT NULL''')

    #TODO - here we need to insert other_features instead of
    # copy_other_features_to_features_db
    for row in ret:
        print("inserting features for", (row[0]))
        features = hv.transform((row[1], row[2]))
        features_diff = features[0] - features[1]
        ret = cf.execute('''INSERT INTO feature_vector(revid, current, parent, diff, is_damaging) VALUES (?, ?, ?, ?, ?)''' ,
                         (
                             row[0],
                             pickle.dumps(features[0]),
                             pickle.dumps(features[1]),
                             pickle.dumps(features_diff),
                             row[4]
                         ))
    return

def get_features_labels_training(consider_other_features = True):
    conn_features = open_db('features.db')
    cf = conn_features.cursor()

    ret = cf.execute('''SELECT other_features, diff, is_damaging FROM feature_vector ORDER BY revid LIMIT 16000''')

    print('fetching')
    rows = ret.fetchall()
    conn_features.close()

    print('zipping')
    other_features, features_vector, labels = zip(*rows)

    count = 0
    print('unpickling')
    features = coo_matrix([])

    for i in features_vector:
        print(count)
        hv_features = pickle.loads(i)

        vector = hv_features
        other_features_coo = coo_matrix([])
        if consider_other_features == True:
            other_features_coo = pickle.loads(other_features[count])
            other_features_coo = list(map(fix_data_type, other_features_coo))
            other_features_coo = coo_matrix([other_features_coo])
            vector = hstack([other_features_coo, hv_features])

        if features.getnnz() == 0:
            features = vstack([vector])
        else:
            features = vstack([features, vector])
            count = count + 1

    print('saving vstacked features')
    joblib.dump(features, 'model_pickled/training_data_features.pkl')
    joblib.dump(labels, 'model_pickled/training_data_labels.pkl')
    return features,labels

def build_model(consider_other_features):
    try:
        features = joblib.load('model_pickled/training_data_features.pkl')
        labels = joblib.load('model_pickled/training_data_labels.pkl')
    except FileNotFoundError:
        features, labels = get_features_labels_training(consider_other_features)

    print('fitting')
    gbc = GradientBoostingClassifier(n_estimators=200, learning_rate=0.05)
    sample_weight=[18939 / (796 + 18939) if l == 'True' else 796 / (796 + 18939) for l in labels]
    gbc.fit(features, labels, sample_weight)

    print('saving')
    joblib.dump(gbc, 'model_pickled/gbc.pkl')
    return gbc

def score_model():
    conn_features = open_db('features.db')
    cf = conn_features.cursor()
    ret = cf.execute('''SELECT diff, is_damaging FROM feature_vector WHERE revid > 646706890 LIMIT 1000''')

    print('fetching')
    rows = ret.fetchall()
    conn_features.close()
    joblib.dump(rows, 'model_pickled/rows_score.pkl')

    print('zipping')
    features_vector, labels = zip(*rows)

    print('unpickling')
    count = 0
    features = coo_matrix([])
    for i in features_vector:
        print(count)
        count = count + 1
        vector = pickle.loads(i)
        if features.getnnz() == 0:
            features = vstack([vector])
        else:
            features = vstack([features, vector])

    del features_vector
    joblib.dump(features, 'model_pickled/features_score.pkl')

    gbc = joblib.load('model_pickled/gbc.pkl')
    score = gbc.score(features.todense(), labels)
    print('score', score)

def score_model_iterative():
    # could not use score method, because when i convert the sparse feature
    # matrix to dense python throws MemoryError

    conn_features = open_db('features.db')
    cf = conn_features.cursor()

    ret = cf.execute('''SELECT revid, other_features, diff, is_damaging FROM feature_vector
    WHERE revid > 646706890 LIMIT 4000''')

    conn_score = open_db('score.db')
    cc = conn_score.cursor()

    gbc = joblib.load('model_pickled/gbc.pkl')
    for row in ret:
        hv_features = pickle.loads(row[2])
        other_features_coo = pickle.loads(row[1])
        other_features_coo = list(map(fix_data_type, other_features_coo))
        other_features_coo = coo_matrix([other_features_coo])
        vector = hstack([other_features_coo, hv_features])

        prediction = gbc.predict(vector.todense())[0]
        #TODO - don't hardcode, calculate the index of the 'True' class
        score_positive = gbc.predict_proba(vector.todense())[0][1]
        classes = gbc.classes_
        print('revid: ', row[0], ', actual: ', row[3], ', prediction', prediction, 'score_positive', score_positive, 'classes', classes)

        cc.execute('''INSERT INTO score
                   (revid, is_damaging_actual, is_damaging_prediction, score_positive)
                   VALUES (?, ?, ?, ?)''', (row[0], row[3], prediction, score_positive))

    # calculate score
    correct_predictions =  cc.execute('''SELECT COUNT(revid) FROM score WHERE is_damaging_actual=is_damaging_prediction''').fetchone()[0]
    total_predictions   =  cc.execute('''SELECT COUNT(revid) FROM score''').fetchone()[0]
    score = (correct_predictions/total_predictions) * 100
    print('Correct Predictions: ', correct_predictions, 'Total Predictions: ', total_predictions, 'Score: ', score)

    # calculate PR-AUC
    rows =  cc.execute('''SELECT is_damaging_actual, score_positive FROM score''').fetchall()
    y_true, y_scores = zip(*rows)
    y_true = [1 if i=='True' else 0 for i in y_true]

    avg_pre = average_precision_score(y_true, list(y_scores))
    roc_auc = roc_auc_score(y_true, list(y_scores))

    print('average precision score: ', avg_pre, 'roc auc score: ', roc_auc)

    conn_features.close()
    conn_score.close()

def example_predictions():
    features = joblib.load('model_pickled/features_score.pkl')
    rows = joblib.load('model_pickled/rows_score.pkl')
    gbc = joblib.load('model_pickled/gbc.pkl')

    features_vector, labels = zip(*rows)
    del features_vector
    for i in range(features.shape[0]):
        print('Actual: ', labels[i], 'Prediction: ', dict(zip(gbc.classes_,
                                                              [int(v*100)
                                                              for v in
                                                              gbc.predict_proba(features.getrow(i).todense())[0]])))
create_sqlite_tables()
export_tsv_to_sqlite()
# download_conents()
# extract_features()
# copy_other_features_to_features_db()
build_model(consider_other_features = False)
# score_model_iterative()
# example_predictions()
