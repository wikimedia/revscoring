import json
import os
import pickle

from revscoring.dependencies import solve
from revscoring.features.meta import aggregators
from revscoring.features.wikibase import session

pwd = os.path.dirname(os.path.realpath(__file__))
ALAN_TURING = json.load(open(os.path.join(pwd, "alan_turing.json")))
ALAN_TURING_OLD = json.load(open(os.path.join(pwd, "alan_turing.old.json")))

revision_entity_doc = session.revisions.datasources.entity_doc
parent_entity_doc = session.revisions.parent.datasources.entity_doc
diff = session.revisions.diff


def test_session_sitelinks_diff():
    cache = {revision_entity_doc: [ALAN_TURING],
             parent_entity_doc: [ALAN_TURING_OLD]}

    sitelinks_diff = solve(diff.datasources.sitelinks_diff, cache=cache)
    assert solve(diff.sitelinks_added, cache=cache) == [26]
    assert (sitelinks_diff[0].added ==
            {'alswiki', 'fowiki', 'itwikiquote', 'commonswiki', 'mgwiki',
             'cywikiquote', 'ruwikiquote', 'kkwiki', 'ttwiki', 'cawikiquote',
             'eswikiquote', 'cewiki', 'cowiki', 'pawiki', 'cswikiquote',
             'hewikiquote', 'newwiki', 'uzwiki', 'zhwikiquote', 'bawiki',
             'furwiki', 'scowiki', 'dewikiquote', 'frwikiquote', 'plwikiquote',
             'enwikiquote'})
    assert solve(diff.sitelinks_removed, cache=cache) == [0]
    assert sitelinks_diff[0].removed == set()
    assert (sitelinks_diff[0].intersection ==
            {'htwiki', 'mtwiki', 'swwiki', 'mkwiki', 'warwiki', 'anwiki', 'rowiki',
             'bgwiki', 'bnwiki', 'orwiki', 'idwiki', 'arwiki', 'skwiki', 'ruewiki',
             'tawiki', 'nnwiki', 'pnbwiki', 'guwiki', 'dewiki', 'cswiki',
             'ilowiki', 'kawiki', 'lvwiki', 'afwiki', 'jvwiki', 'zh_yuewiki',
             'tgwiki', 'hrwiki', 'brwiki', 'iswiki', 'ruwiki', 'dawiki', 'eswiki',
             'ltwiki', 'fawiki', 'bewiki', 'glwiki', 'iowiki', 'vowiki', 'yiwiki',
             'yowiki', 'plwiki', 'be_x_oldwiki', 'mlwiki', 'mswiki', 'astwiki',
             'hifwiki', 'urwiki', 'hewiki', 'aswiki', 'ocwiki', 'sawiki', 'cawiki',
             'tewiki', 'hiwiki', 'shwiki', 'pmswiki', 'trwiki', 'zh_min_nanwiki',
             'tlwiki', 'knwiki', 'jawiki', 'arzwiki', 'cywiki', 'lijwiki',
             'ptwiki', 'zhwiki', 'viwiki', 'mwlwiki', 'nlwiki', 'kowiki',
             'ganwiki', 'lawiki', 'simplewiki', 'bswiki', 'etwiki', 'slwiki',
             'huwiki', 'hywiki', 'sqwiki', 'srwiki', 'liwiki', 'lbwiki', 'fywiki',
             'mnwiki', 'fiwiki', 'lmowiki', 'jbowiki', 'thwiki', 'sahwiki',
             'euwiki', 'gawiki', 'azwiki', 'elwiki', 'kuwiki', 'ukwiki',
             'bat_smgwiki', 'pamwiki', 'mrwiki', 'enwiki', 'ckbwiki', 'frwiki',
             'eowiki', 'svwiki', 'gdwiki', 'scnwiki', 'itwiki', 'nowiki'})
    assert solve(diff.sitelinks_changed, cache=cache) == [2]
    assert sitelinks_diff[0].changed == {'skwiki', 'sahwiki'}
    assert (sitelinks_diff[0].unchanged ==
            {'warwiki', 'aswiki', 'cywiki', 'lvwiki', 'sawiki', 'zh_yuewiki',
             'tewiki', 'pnbwiki', 'idwiki', 'mlwiki', 'anwiki', 'pmswiki',
             'kawiki', 'ptwiki', 'iowiki', 'ltwiki', 'bat_smgwiki', 'cswiki',
             'swwiki', 'rowiki', 'mswiki', 'etwiki', 'jvwiki', 'dawiki',
             'hifwiki', 'euwiki', 'simplewiki', 'htwiki', 'srwiki', 'huwiki',
             'bswiki', 'ilowiki', 'brwiki', 'hrwiki', 'eswiki', 'yiwiki', 'bnwiki',
             'glwiki', 'zhwiki', 'hiwiki', 'tawiki', 'eowiki', 'kowiki', 'yowiki',
             'jawiki', 'scnwiki', 'slwiki', 'astwiki', 'lijwiki', 'nnwiki',
             'svwiki', 'ruwiki', 'tlwiki', 'bgwiki', 'pamwiki', 'sqwiki', 'tgwiki',
             'gdwiki', 'fiwiki', 'mwlwiki', 'mnwiki', 'lmowiki', 'ukwiki',
             'arwiki', 'hewiki', 'enwiki', 'orwiki', 'lbwiki', 'thwiki', 'fywiki',
             'knwiki', 'elwiki', 'frwiki', 'shwiki', 'itwiki', 'azwiki',
             'zh_min_nanwiki', 'gawiki', 'liwiki', 'iswiki', 'trwiki', 'cawiki',
             'nlwiki', 'be_x_oldwiki', 'kuwiki', 'lawiki', 'bewiki', 'guwiki',
             'urwiki', 'nowiki', 'fawiki', 'jbowiki', 'ruewiki', 'afwiki',
             'arzwiki', 'ganwiki', 'ckbwiki', 'ocwiki', 'plwiki', 'dewiki',
             'viwiki', 'hywiki', 'mkwiki', 'mrwiki', 'mtwiki', 'vowiki'})

    assert (pickle.loads(pickle.dumps(diff.datasources.sitelinks_diff)) ==
            diff.datasources.sitelinks_diff)


def test_entity():
    assert solve(session.revisions.datasources.entity,
                 cache={revision_entity_doc: [None]})[0].properties == {}

    solve(session.revisions.datasources.entity,
          cache={revision_entity_doc: [ALAN_TURING]})

    assert (pickle.loads(pickle.dumps(session.revisions.datasources.entity)) ==
            session.revisions.datasources.entity)

    assert solve(session.revisions.properties,
                 cache={revision_entity_doc: [ALAN_TURING]}) == [57]
    assert solve(aggregators.sum(session.revisions.properties),
                 cache={revision_entity_doc: [ALAN_TURING]}) == 57
    assert (solve(session.revisions.datasources.properties,
                  cache={revision_entity_doc: [ALAN_TURING]})[0].keys() ==
            {'P1430', 'P906', 'P1816', 'P570', 'P31', 'P1343', 'P2021', 'P535',
             'P800', 'P569', 'P373', 'P1819', 'P108', 'P227', 'P185', 'P910',
             'P1273', 'P69', 'P244', 'P20', 'P101', 'P106', 'P18', 'P1563', 'P25',
             'P646', 'P1296', 'P214', 'P950', 'P463', 'P1006', 'P268', 'P21',
             'P1417', 'P22', 'P1207', 'P19', 'P91', 'P735', 'P1412', 'P166',
             'P269', 'P1741', 'P1196', 'P27', 'P140', 'P512', 'P1415', 'P691',
             'P345', 'P949', 'P1263', 'P549', 'P184', 'P935', 'P349', 'P213'})
