import json
import os
import pickle

from nose.tools import eq_

from .. import diff, parent_revision, revision
from ....dependencies import solve

pwd = os.path.dirname(os.path.realpath(__file__))
ALAN_TOURING = json.load(open(os.path.join(pwd, "alan_touring.json")))
ALAN_TOURING_OLD = json.load(open(os.path.join(pwd, "alan_touring.old.json")))


def test_sitelinks_diff():
    cache = {revision.item_doc: ALAN_TOURING,
             parent_revision.item_doc: ALAN_TOURING_OLD}

    sitelinks_diff = solve(diff.sitelinks_diff, cache=cache)
    eq_(sitelinks_diff.added,
        {'alswiki', 'fowiki', 'itwikiquote', 'commonswiki', 'mgwiki',
         'cywikiquote', 'ruwikiquote', 'kkwiki', 'ttwiki', 'cawikiquote',
         'eswikiquote', 'cewiki', 'cowiki', 'pawiki', 'cswikiquote',
         'hewikiquote', 'newwiki', 'uzwiki', 'zhwikiquote', 'bawiki',
         'furwiki', 'scowiki', 'dewikiquote', 'frwikiquote', 'plwikiquote',
         'enwikiquote'})
    eq_(sitelinks_diff.removed, set())
    eq_(sitelinks_diff.intersection,
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
    eq_(sitelinks_diff.changed, {'skwiki', 'sahwiki'})
    eq_(sitelinks_diff.unchanged,
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

    eq_(pickle.loads(pickle.dumps(diff.sitelinks_diff)), diff.sitelinks_diff)


def test_labels_diff():
    cache = {revision.item_doc: ALAN_TOURING,
             parent_revision.item_doc: ALAN_TOURING_OLD}

    labels_diff = solve(diff.labels_diff, cache=cache)
    eq_(labels_diff.added,
        {'tt', 'fo', 'pa', 'nan', 'sgs', 'mg', 'zh-cn', 'ba', 'fur', 'sco',
         'co', 'gsw', 'uz', 'kk', 'zh-hans', 'new', 'ce', 'de-ch'})
    eq_(labels_diff.removed,
        {'simple', 'zh-yue', 'bat-smg', 'be-x-old', 'zh-min-nan', 'no'})
    eq_(labels_diff.intersection,
        {'jv', 'gl', 'te', 'war', 'pt', 'de', 'gd', 'sq', 'lv', 'hif', 'hy',
         'hr', 'rue', 'pnb', 'ca', 'ka', 'nl', 'sr', 'gan', 'ur', 'vi', 'bg',
         'scn', 'th', 'ast', 'az', 'tl', 'mr', 'af', 'zh', 'ko', 'be', 'ja',
         'ml', 'ilo', 'oc', 'cs', 'lb', 'yue', 'fi', 'sw', 'pl', 'es', 'eo',
         'arz', 'nb', 'nn', 'ru', 'tr', 'mk', 'sa', 'en-gb', 'mn', 'br',
         'sah', 'ro', 'yo', 'is', 'el', 'jbo', 'he', 'en', 'hi', 'bs', 'id',
         'gu', 'sv', 'lmo', 'pt-br', 'an', 'kn', 'ar', 'it', 'mt', 'tg', 'io',
         'ms', 'sh', 'eu', 'or', 'li', 'pam', 'pms', 'la', 'mwl', 'lij', 'da',
         'vo', 'fr', 'uk', 'fy', 'lt', 'bn', 'et', 'ku', 'ht', 'yi', 'ckb',
         'sk', 'fa', 'hu', 'as', 'be-tarask', 'ta', 'ga', 'sl', 'cy', 'en-ca'})
    eq_(labels_diff.changed, {'ru', 'eo'})
    eq_(labels_diff.unchanged,
        {'ml', 'nn', 'hif', 'hr', 'hu', 'ar', 'ka', 'ko', 'vi', 'he', 'jbo',
         'sah', 'as', 'bs', 'ht', 'pam', 'scn', 'tr', 'tg', 'mr', 'mwl', 'nl',
         'io', 'rue', 'es', 'el', 'pnb', 'sq', 'nb', 'sk', 'ja', 'mt', 'de',
         'arz', 'it', 'sw', 'kn', 'ku', 'sa', 'or', 'sr', 'pt', 'zh', 'af',
         'cy', 'th', 'pt-br', 'hi', 'pms', 'jv', 'ta', 'fa', 'sl', 'fr', 'yo',
         'lij', 'li', 'en-gb', 'sv', 'hy', 'bg', 'lb', 'en', 'fi', 'lmo',
         'az', 'da', 'te', 'eu', 'ast', 'ms', 'gan', 'ca', 'la', 'ro', 'uk',
         'mn', 'mk', 'lt', 'vo', 'is', 'et', 'br', 'fy', 'yue', 'be', 'yi',
         'ga', 'bn', 'sh', 'gl', 'cs', 'ckb', 'ur', 'tl', 'pl', 'lv', 'id',
         'gd', 'war', 'gu', 'an', 'oc', 'en-ca', 'be-tarask', 'ilo'})

    eq_(pickle.loads(pickle.dumps(diff.labels_diff)), diff.labels_diff)


def test_aliases_diff():
    cache = {revision.item_doc: ALAN_TOURING,
             parent_revision.item_doc: ALAN_TOURING_OLD}

    aliases_diff = solve(diff.aliases_diff, cache=cache)
    eq_(aliases_diff.added,
        {'ko', 'ru'})
    eq_(aliases_diff.removed, set())
    eq_(aliases_diff.intersection,
        {'ja', 'fr', 'de', 'be-tarask', 'jbo', 'en', 'it'})
    eq_(aliases_diff.changed, set())
    eq_(aliases_diff.unchanged,
        {'en', 'be-tarask', 'de', 'jbo', 'it', 'fr', 'ja'})

    eq_(pickle.loads(pickle.dumps(diff.aliases_diff)), diff.aliases_diff)


def test_descriptions_diff():
    cache = {revision.item_doc: ALAN_TOURING,
             parent_revision.item_doc: ALAN_TOURING_OLD}

    descriptions_diff = solve(diff.descriptions_diff, cache=cache)
    eq_(descriptions_diff.added,
        {'da', 'sk', 'as', 'zh-cn', 'pl', 'ru', 'nl', 'zh', 'gl', 'nn', 'pam',
         'nb', 'sv', 'ko', 'zh-hans'})
    eq_(descriptions_diff.removed, set())
    eq_(descriptions_diff.intersection,
        {'en', 'it', 'fr', 'es', 'ilo', 'fa', 'de'})
    eq_(descriptions_diff.changed, {'fa'})
    eq_(descriptions_diff.unchanged, {'fr', 'it', 'es', 'de', 'en', 'ilo'})

    eq_(pickle.loads(pickle.dumps(diff.descriptions_diff)),
        diff.descriptions_diff)


def test_claims_diff():
    cache = {revision.item_doc: ALAN_TOURING,
             parent_revision.item_doc: ALAN_TOURING_OLD}

    claims_diff = solve(diff.claims_diff, cache=cache)
    eq_(claims_diff.added,
        {'P31', 'P1741', 'P950', 'P935', 'P27', 'P1296', 'P1415', 'P1207',
         'P549', 'P512', 'P1343', 'P906', 'P1816', 'P735', 'P25', 'P1417',
         'P1412', 'P691', 'P949', 'P800', 'P1273', 'P1196', 'P1819', 'P646',
         'P140', 'P1563', 'P1430', 'P345', 'P1263', 'P1006', 'P166', 'P2021',
         'P910', 'P108', 'P22'})
    eq_(claims_diff.removed, {'P509', 'P107'})
    eq_(claims_diff.intersection,
        {'P69', 'P268', 'P213', 'P106', 'P20', 'P19', 'P214', 'P269', 'P91',
         'P570', 'P18', 'P185', 'P227', 'P101', 'P463', 'P535', 'P373', 'P184',
         'P244', 'P21', 'P349', 'P569'})
    eq_(claims_diff.changed,
        {'P19', 'P570', 'P91', 'P569', 'P20', 'P227', 'P101', 'P69', 'P21',
         'P106'})
    eq_(claims_diff.unchanged,
        {'P244', 'P269', 'P268', 'P535', 'P18', 'P373', 'P185', 'P213', 'P463',
         'P349', 'P184', 'P214'})

    eq_(pickle.loads(pickle.dumps(diff.claims_diff)), diff.claims_diff)


def test_badges_diff():
    cache = {revision.item_doc: ALAN_TOURING,
             parent_revision.item_doc: ALAN_TOURING_OLD}

    badges_diff = solve(diff.badges_diff, cache=cache)
    eq_(badges_diff.added, {'lawiki', 'aswiki', 'enwiki', 'ruwiki', 'azwiki'})
    eq_(badges_diff.removed, set())
    eq_(badges_diff.intersection, set())
    eq_(badges_diff.changed, set())
    eq_(badges_diff.unchanged, set())

    eq_(pickle.loads(pickle.dumps(diff.badges_diff)), diff.badges_diff)
