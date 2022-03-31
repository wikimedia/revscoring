import os
import pickle
import pytest

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.features.wikibase.revision_oriented import revision
from revscoring.errors import UnexpectedContentType

pwd = os.path.dirname(os.path.realpath(__file__))
ALAN_TEXT = open(os.path.join(pwd, "alan_turing.json")).read()

r_text = revision_oriented.revision.text

has_p106 = revision.has_property('P106')
has_p999 = revision.has_property('P999')

has_p106_q82594 = revision.has_property_value('P106', "Q82594")
has_p106_test = revision.has_property_value('P106', "Test")
has_p999_foo = revision.has_property_value('P999', "Foo")


def test_entity_doc():
    solve(revision.datasources.entity_doc, cache={r_text: ALAN_TEXT})
    assert solve(revision.datasources.entity_doc, cache={r_text: None}) is None

    assert (pickle.loads(pickle.dumps(revision.datasources.entity_doc)) ==
            revision.datasources.entity_doc)

    with pytest.raises(UnexpectedContentType):
        solve(revision.datasources.entity_doc, cache={r_text:
                "unexpected content type"})

def test_entity():
    entity = solve(revision.datasources.entity, cache={r_text: None})
    assert entity.properties == {}

    solve(revision.datasources.entity, cache={r_text: ALAN_TEXT})

    assert (pickle.loads(pickle.dumps(revision.datasources.entity)) ==
            revision.datasources.entity)

    assert solve(revision.properties, cache={r_text: ALAN_TEXT}) == 57
    assert (solve(revision.datasources.properties,
                  cache={r_text: ALAN_TEXT}).keys() ==
            {'P1430', 'P906', 'P1816', 'P570', 'P31', 'P1343', 'P2021', 'P535',
             'P800', 'P569', 'P373', 'P1819', 'P108', 'P227', 'P185', 'P910',
             'P1273', 'P69', 'P244', 'P20', 'P101', 'P106', 'P18', 'P1563',
             'P25', 'P646', 'P1296', 'P214', 'P950', 'P463', 'P1006', 'P268',
             'P21', 'P1417', 'P22', 'P1207', 'P19', 'P91', 'P735', 'P1412',
             'P166', 'P269', 'P1741', 'P1196', 'P27', 'P140', 'P512', 'P1415',
             'P691', 'P345', 'P949', 'P1263', 'P549', 'P184', 'P935', 'P349',
             'P213'})

    assert solve(revision.claims, cache={r_text: ALAN_TEXT}) == 71
    assert (solve(revision.datasources.claims, cache={r_text: ALAN_TEXT}) ==
            {('P1430', "'368'"), ('P1412', 'Q1860'),
             ('P691', "'jn19990008646'"), ('P935', "'Alan Turing'"),
             ('P25', 'Q20895935'), ('P1263', "'952/000023883'"),
             ('P166', 'Q15631401'), ('P949', "'000133188'"),
             ('P569', '+1912-06-23T00:00:00Z'), ('P512', 'Q230899'),
             ('P166', 'Q10762848'), ('P1207', "'n98045497'"),
             ('P1816', "'mp18700'"), ('P373', "'Alan Turing'"),
             ('P69', 'Q924289'), ('P950', "'XX945020'"),
             ('P244', "'n83171546'"), ('P800', 'Q20895949'),
             ('P1296', "'0067958'"), ('P106', 'Q82594'), ('P800', 'Q772056'),
             ('P800', 'Q20895966'), ('P1006', "'070580685'"),
             ('P101', 'Q897511'), ('P140', 'Q7066'),
             ('P213', "'0000 0001 1058 9902'"), ('P1819', "'I00586443'"),
             ('P19', 'Q20895942'), ('P269', "'030691621'"),
             ('P108', 'Q220798'), ('P22', 'Q20895930'),
             ('P2021', '5 (5-5) 1'), ('P185', 'Q249984'),
             ('P106', 'Q81096'), ('P549', "'8014'"), ('P1343', 'Q2627728'),
             ('P1741', "'226316'"), ('P268', "'12205670t'"),
             ('P1563', "'Turing'"), ('P106', 'Q11513337'),
             ('P570', '+1954-06-07T00:00:00Z'), ('P512', 'Q21578'),
             ('P69', 'Q2278254'), ('P31', 'Q5'), ('P227', "'118802976'"),
             ('P1196', 'Q10737'), ('P108', 'Q230899'), ('P21', 'Q6581097'),
             ('P1417', "'609739'"), ('P1343', 'Q17329836'),
             ('P349', "'00621580'"), ('P535', "'12651680'"),
             ('P463', 'Q123885'), ('P101', 'Q21198'), ('P91', 'Q6636'),
             ('P345', "'nm6290133'"), ('P735', 'Q294833'),
             ('P214', "'41887917'"), ('P906', "'254262'"),
             ('P910', 'Q9384007'), ('P27', 'Q145'), ('P106', 'Q170790'),
             ('P184', 'Q92741'), ('P646', "'/m/0n00'"),
             ('P18', "'Alan Turing Aged 16.jpg'"), ('P19', 'Q122744'),
             ('P106', 'Q4964182'), ('P69', 'Q21578'), ('P20', 'Q2011497'),
             ('P1273', "'a11455408'"), ('P1415', "'101036578'")})
    assert solve(revision.aliases, cache={r_text: ALAN_TEXT}) == 9
    assert (solve(revision.datasources.aliases, cache={r_text: ALAN_TEXT}) ==
            {'de': ['Alan Mathison Turing'], 'en': ['Alan Mathison Turing'],
             'fr': ['Alan Mathison Turing'], 'ru': ['Тьюринг, Алан'],
             'jbo': ['alan turin'], 'it': ['Alan Mathison Turing'],
             'ko': ['앨런 매티슨 튜링'],
             'be-tarask': ["Элан Т'юрынг", 'Алан Цюрынг', "Т'юрынг"],
             'ja': ['アラン・テューリング']})
    assert solve(revision.sources, cache={r_text: ALAN_TEXT}) == 56
    assert (solve(revision.datasources.sources, cache={r_text: ALAN_TEXT}) ==
            {('P108', 'Q220798', 'P248', 'Q20895922'),
             ('P106', 'Q4964182', 'P143', 'Q48952'),
             ('P69', 'Q924289', 'P248', 'Q20895922'),
             ('P570', '+1954-06-07T00:00:00Z', 'P143', 'Q206855'),
             ('P31', 'Q5', 'P248', 'Q20666306'),
             ('P800', 'Q20895949', 'P248', 'Q20895922'),
             ('P25', 'Q20895935', 'P248', 'Q20895922'),
             ('P349', "'00621580'", 'P143', 'Q48183'),
             ('P549', "'8014'", 'P143', 'Q328'),
             ('P569', '+1912-06-23T00:00:00Z', 'P854',
              "'http://data.bnf.fr/ark:/12148/cb12205670t'"),
             ('P18', "'Alan Turing Aged 16.jpg'", 'P143', 'Q11920'),
             ('P569', '+1912-06-23T00:00:00Z', 'P248', 'Q20666306'),
             ('P19', 'Q122744', 'P143', 'Q328'),
             ('P214', "'41887917'", 'P143', 'Q8447'),
             ('P569', '+1912-06-23T00:00:00Z', 'P143', 'Q328'),
             ('P569', '+1912-06-23T00:00:00Z', 'P345', "'nm6290133'"),
             ('P91', 'Q6636', 'P248', 'Q20895922'),
             ('P1273', "'a11455408'", 'P854',
              "'https://viaf.org/viaf/41887917/'"),
             ('P1412', 'Q1860', 'P143', 'Q20666306'),
             ('P69', 'Q2278254', 'P248', 'Q20895922'),
             ('P31', 'Q5', 'P813', '+2015-10-10T00:00:00Z'),
             ('P512', 'Q230899', 'P143', 'Q8447'),
             ('P512', 'Q21578', 'P143', 'Q8447'),
             ('P1412', 'Q1860', 'P813', '+2015-10-10T00:00:00Z'),
             ('P1412', 'Q1860', 'P854',
              "'http://data.bnf.fr/ark:/12148/cb12205670t'"),
             ('P535', "'12651680'", 'P143', 'Q328'),
             ('P19', 'Q20895942', 'P248', 'Q20895922'),
             ('P227', "'118802976'", 'P143', 'Q1419226'),
             ('P570', '+1954-06-07T00:00:00Z', 'P248', 'Q20666306'),
             ('P21', 'Q6581097', 'P143', 'Q54919'),
             ('P800', 'Q20895966', 'P248', 'Q20895922'),
             ('P935', "'Alan Turing'", 'P143', 'Q191168'),
             ('P31', 'Q5', 'P143', 'Q206855'),
             ('P21', 'Q6581097', 'P248', 'Q36578'),
             ('P646', "'/m/0n00'", 'P248', 'Q15241312'),
             ('P646', "'/m/0n00'", 'P577', '+2013-10-28T00:00:00Z'),
             ('P1563', "'Turing'", 'P143', 'Q11921'),
             ('P19', 'Q122744', 'P854',
              "'http://www.telegraph.co.uk/technology/news/9314910/Britain-still-owes-Alan-Turing-a-debt.html'"), # noqa
             ('P269', "'030691621'", 'P143', 'Q8447'),
             ('P108', 'Q230899', 'P248', 'Q20895922'),
             ('P22', 'Q20895930', 'P248', 'Q20895922'),
             ('P906', "'254262'", 'P143', 'Q877583'),
             ('P21', 'Q6581097', 'P813', '+2014-04-09T00:00:00Z'),
             ('P244', "'n83171546'", 'P143', 'Q328'),
             ('P570', '+1954-06-07T00:00:00Z', 'P854',
              "'http://data.bnf.fr/ark:/12148/cb12205670t'"),
             ('P570', '+1954-06-07T00:00:00Z', 'P813',
              '+2015-10-10T00:00:00Z'),
             ('P106', 'Q82594', 'P143', 'Q328'),
             ('P570', '+1954-06-07T00:00:00Z', 'P345', "'nm6290133'"),
             ('P213', "'0000 0001 1058 9902'", 'P143', 'Q423048'),
             ('P31', 'Q5', 'P854',
              "'http://data.bnf.fr/ark:/12148/cb12205670t'"),
             ('P569', '+1912-06-23T00:00:00Z', 'P813',
              '+2015-10-10T00:00:00Z'),
             ('P1196', 'Q10737', 'P248', 'Q20895922'),
             ('P268', "'12205670t'", 'P143', 'Q8447'),
             ('P800', 'Q772056', 'P248', 'Q20895922'),
             ('P20', 'Q2011497', 'P248', 'Q20895922'),
             ('P27', 'Q145', 'P143', 'Q48183')})
    assert solve(revision.qualifiers, cache={r_text: ALAN_TEXT}) == 6
    assert (solve(revision.datasources.qualifiers, cache={r_text: ALAN_TEXT}) ==
            {('P1343', 'Q17329836', 'P854', 0,
              "'http://www.larousse.fr/encyclopedie/personnage/Alan_Mathison_Turing/147690'"), # noqa
             ('P108', 'Q220798', 'P580', 0, '+1938-00-00T00:00:00Z'),
             ('P1343', 'Q2627728', 'P854', 0,
              "'http://krugosvet.ru/enc/gumanitarnye_nauki/lingvistika/TYURING_ALAN_MATISON.html'"), # noqa
             ('P108', 'Q220798', 'P582', 0, '+1945-00-00T00:00:00Z'),
             ('P108', 'Q230899', 'P580', 0, '+1948-03-00T00:00:00Z'),
             ('P69', 'Q2278254', 'P580', 0, '+1926-00-00T00:00:00Z')})

    assert solve(revision.badges, cache={r_text: ALAN_TEXT}) == 5
    assert (solve(revision.datasources.badges, cache={r_text: ALAN_TEXT}) ==
            {'aswiki': ['Q17437798'], 'ruwiki': ['Q17437798'],
             'azwiki': ['Q17437796'], 'lawiki': ['Q17437796'],
             'enwiki': ['Q17437798']})
    assert solve(revision.labels, cache={r_text: ALAN_TEXT}) == 126
    assert (solve(revision.datasources.labels, cache={r_text: ALAN_TEXT}) ==
            {'th': 'แอลัน ทัวริง', 'is': 'Alan Turing', 'ku': 'Alan Turing',
             'sgs': 'Alans Tiorėngs', 'ar': 'آلان تورنج', 'kk': 'Алан Тьюринг',
             'yue': '圖靈', 'ta': 'அலன் டூரிங்', 'cs': 'Alan Turing',
             'li': 'Alan Turing', 'bn': 'অ্যালান টুরিং', 'sl': 'Alan Turing',
             'gsw': 'Alan Turing', 'sv': 'Alan Turing', 'hif': 'Alan Turing',
             'en-gb': 'Alan Turing', 'en': 'Alan Turing', 'az': 'Alan Türinq',
             'ja': 'アラン・チューリング', 'oc': 'Alan Turing',
             'pt-br': 'Alan Turing', 'da': 'Alan Turing', 'ca': 'Alan Turing',
             'eo': 'Alan TURING', 'el': 'Άλαν Τούρινγκ', 'yi': 'עלן טיורינג',
             'nan': 'Alan Turing', 'sh': 'Alan Turing', 'as': 'এলান ট্যুৰিং',
             'hy': 'Ալան Թյուրինգ', 'fa': 'آلن تورینگ', 'en-ca': 'Alan Turing',
             'tr': 'Alan Turing', 'mn': 'Алан Матисон Тюринг',
             'he': 'אלן טיורינג', 'scn': 'Alan Turing', 'vo': 'Alan Turing',
             'yo': 'Alan Turing', 'et': 'Alan Turing', 'ur': 'ایلن تورنگ',
             'fo': 'Alan Turing', 'io': 'Alan Turing', 'ilo': 'Alan Turing',
             'ru': 'Алан Тьюринг', 'gl': 'Alan Turing', 'war': 'Alan Turing',
             'kn': 'ಅಲೆನ್ ಟ್ಯೂರಿಂಗ್', 'uz': 'Tyuring', 'de': 'Alan Turing',
             'zh-cn': '艾伦·图灵', 'la': 'Alanus Mathison Turing',
             'sk': 'Alan Mathison Turing', 'mk': 'Алан Тјуринг',
             'hr': 'Alan Turing', 'uk': 'Алан Тюрінг', 'pl': 'Alan Turing',
             'ro': 'Alan Turing', 'nl': 'Alan Turing', 'nb': 'Alan Turing',
             'br': 'Alan Turing', 'fr': 'Alan Turing', 'mt': 'Alan Turing',
             'it': 'Alan Turing', 'ce': 'Тьюринг, Алан',
             'te': 'అలాన్ ట్యూరింగ్\u200c', 'fi': 'Alan Turing',
             'pa': 'ਅਲਾਨ ਟੂਰਿੰਗ',
             'nn': 'Alan Turing', 'zh-hans': '艾伦·图灵', 'af': 'Alan Turing',
             'be': 'Алан Матысан Цьюрынг', 'ga': 'Alan Turing',
             'ckb': 'ئالان تیورینگ', 'es': 'Alan Turing', 'arz': 'الان تورينج',
             'new': 'एलेन त्युरिङ्ग', 'tt': 'Alan Tyuring',
             'ht': 'Alan Turing',
             'cy': 'Alan Turing', 'mwl': 'Alan Turing', 'or': 'ଆଲାନ ଟ୍ୟୁରିଙ୍ଗ',
             'jbo': '.alan turin', 'ml': 'അലൻ ട്യൂറിംഗ്',
             'sa': 'एलेन ट्यूरिंग',
             'bs': 'Alan Turing', 'tg': 'Алан Тюринг', 'ms': 'Alan Turing',
             'lv': 'Alans Tjūrings', 'fur': 'Alan Turing',
             'sco': 'Alan Turing',
             'sah': 'Алан Матисон Тьюринг', 'lmo': 'Alan Turing',
             'mr': 'ॲलन ट्युरिंग', 'pnb': 'الان ٹورنگ', 'eu': 'Alan Turing',
             'zh': '艾伦·图灵', 'de-ch': 'Alan Turing', 'gu': 'ઍલન ટ્યુરિંગ',
             'gan': '圖靈', 'sw': 'Alan Turing', 'mg': 'Alan Turing',
             'be-tarask': 'Элан Т’юрынг', 'hu': 'Alan Turing',
             'lij': 'Alan Turing', 'an': 'Alan Turing', 'pt': 'Alan Turing',
             'pms': 'Alan Turing', 'gd': 'Alan Turing', 'lt': 'Alan Turing',
             'jv': 'Alan Turing', 'fy': 'Alan Turing', 'sq': 'Alan Turing',
             'ka': 'ალან ტიურინგი', 'vi': 'Alan Turing', 'sr': 'Алан Тјуринг',
             'pam': 'Alan Turing', 'ast': 'Alan Turing', 'co': 'Alanu Turing',
             'ko': '앨런 튜링', 'tl': 'Alan Turing', 'rue': 'Алан Тюрінґ',
             'lb': 'Alan M. Turing', 'id': 'Alan Turing', 'bg': 'Алън Тюринг',
             'ba': 'Алан Тьюринг', 'hi': 'एलेन ट्यूरिंग'})
    assert solve(revision.sitelinks, cache={r_text: ALAN_TEXT}) == 134
    assert (solve(revision.datasources.sitelinks, cache={r_text: ALAN_TEXT}) ==
            {'mrwiki': 'ॲलन ट्युरिंग', 'warwiki': 'Alan Turing',
             'mkwiki': 'Алан Тјуринг', 'bawiki': 'Алан Тьюринг',
             'mnwiki': 'Алан Матисон Тюринг', 'mgwiki': 'Alan Turing',
             'tawiki': 'அலன் டூரிங்', 'yowiki': 'Alan Turing',
             'ttwiki': 'Alan Tyuring', 'ruewiki': 'Алан Тюрінґ',
             'gdwiki': 'Alan Turing', 'liwiki': 'Alan Turing', 'pamwiki':
             'Alan Turing', 'scnwiki': 'Alan Turing', 'scowiki': 'Alan Turing',
             'fowiki': 'Alan Turing', 'fywiki': 'Alan Turing',
             'bnwiki': 'অ্যালান টুরিং', 'jbowiki': '.alan turin',
             'guwiki': 'ઍલન ટ્યુરિંગ', 'knwiki': 'ಅಲೆನ್ ಟ್ಯೂರಿಂಗ್',
             'dewiki': 'Alan Turing', 'be_x_oldwiki': 'Элан Т’юрынг',
             'eswiki': 'Alan Turing', 'hrwiki': 'Alan Turing',
             'mwlwiki': 'Alan Turing', 'afwiki': 'Alan Turing',
             'sqwiki': 'Alan Turing', 'mtwiki': 'Alan Turing',
             'cawiki': 'Alan Turing', 'zh_min_nanwiki': 'Alan Turing',
             'trwiki': 'Alan Turing', 'hiwiki': 'एलेन ट्यूरिंग',
             'nlwiki': 'Alan Turing', 'cswikiquote': 'Alan Turing',
             'azwiki': 'Alan Türinq', 'kkwiki': 'Алан Тьюринг',
             'plwikiquote': 'Alan Turing', 'hywiki': 'Ալան Թյուրինգ',
             'cewiki': 'Тьюринг, Алан', 'nnwiki': 'Alan Turing',
             'ruwikiquote': 'Алан Матисон Тьюринг', 'tgwiki': 'Алан Тюринг',
             'commonswiki': 'Alan Turing', 'lawiki': 'Alanus Mathison Turing',
             'itwiki': 'Alan Turing', 'eowiki': 'Alan Turing',
             'dawiki': 'Alan Turing', 'kowiki': '앨런 튜링',
             'bewiki': 'Алан Матысан Цьюрынг', 'rowiki': 'Alan Turing',
             'ocwiki': 'Alan Turing', 'newwiki': 'एलेन त्युरिङ्ग',
             'lbwiki': 'Alan M. Turing', 'pawiki': 'ਅਲਾਨ ਟੂਰਿੰਗ',
             'enwikiquote': 'Alan Turing', 'hifwiki': 'Alan Turing',
             'mlwiki': 'അലൻ ട്യൂറിംഗ്', 'jawiki': 'アラン・チューリング',
             'viwiki': 'Alan Turing', 'htwiki': 'Alan Turing',
             'furwiki': 'Alan Turing', 'zhwikiquote': '艾伦·图灵',
             'lijwiki': 'Alan Turing', 'plwiki': 'Alan Turing',
             'vowiki': 'Alan Turing', 'bswiki': 'Alan Turing',
             'tewiki': 'అలాన్ ట్యూరింగ్\u200c', 'sawiki': 'एलेन ट्यूरिंग',
             'ptwiki': 'Alan Turing', 'urwiki': 'ایلن تورنگ',
             'arwiki': 'آلان تورنج', 'iswiki': 'Alan Turing',
             'huwiki': 'Alan Turing', 'tlwiki': 'Alan Turing',
             'uzwiki': 'Alan Tyuring', 'frwikiquote': 'Alan Turing',
             'zh_yuewiki': '圖靈', 'pnbwiki': 'الان ٹورنگ',
             'dewikiquote': 'Alan Turing', 'swwiki': 'Alan Turing',
             'itwikiquote': 'Alan Turing', 'lvwiki': 'Alans Tjūrings',
             'anwiki': 'Alan Turing', 'aswiki': 'এলান ট্যুৰিং',
             'arzwiki': 'الان تورينج', 'srwiki': 'Алан Тјуринг',
             'eswikiquote': 'Alan Mathison Turing', 'elwiki': 'Άλαν Τούρινγκ',
             'frwiki': 'Alan Turing', 'brwiki': 'Alan Turing',
             'fiwiki': 'Alan Turing', 'fawiki': 'آلن تورینگ',
             'ilowiki': 'Alan Turing', 'cswiki': 'Alan Turing',
             'kawiki': 'ალან ტიურინგი', 'yiwiki': 'עלן טיורינג',
             'gawiki': 'Alan Turing', 'skwiki': 'Alan Turing',
             'shwiki': 'Alan Turing', 'sahwiki': 'Тьюринг Алан Матисон',
             'ukwiki': 'Алан Тюрінг', 'bat_smgwiki': 'Alans Tiorėngs',
             'hewiki': 'אלן טיורינג', 'enwiki': 'Alan Turing',
             'bgwiki': 'Алън Тюринг', 'svwiki': 'Alan Turing',
             'orwiki': 'ଆଲାନ ଟ୍ୟୁରିଙ୍ଗ', 'lmowiki': 'Alan Turing',
             'glwiki': 'Alan Turing', 'mswiki': 'Alan Turing',
             'zhwiki': '艾伦·图灵', 'alswiki': 'Alan Turing',
             'etwiki': 'Alan Turing', 'jvwiki': 'Alan Turing',
             'hewikiquote': 'אלן טיורינג', 'astwiki': 'Alan Turing',
             'kuwiki': 'Alan Turing', 'cywikiquote': 'Alan Turing',
             'idwiki': 'Alan Turing', 'thwiki': 'แอลัน ทัวริง',
             'pmswiki': 'Alan Turing', 'ruwiki': 'Тьюринг, Алан',
             'iowiki': 'Alan Turing', 'nowiki': 'Alan Turing',
             'cywiki': 'Alan Turing', 'euwiki': 'Alan Turing',
             'ltwiki': 'Alan Turing', 'cawikiquote': 'Alan Turing',
             'simplewiki': 'Alan Turing', 'cowiki': 'Alanu Turing',
             'ganwiki': '圖靈', 'ckbwiki': 'ئالان تیورینگ',
             'slwiki': 'Alan Turing'})
    assert solve(revision.descriptions, cache={r_text: ALAN_TEXT}) == 22
    assert (solve(revision.datasources.descriptions, cache={r_text: ALAN_TEXT}) ==
            {'da': 'britisk informatiker, matematiker og ingeniør',
             'ko': '영국의 수학자, 논리학자, 암호해독학자, 컴퓨터 과학자',
             'it': 'matematico, logico e crittografo britannico',
             'fr': 'mathématicien britannique',
             'nn': 'britisk informatikar, matematikar og ingeniør',
             'gl': 'matemático, filósofo e criptógrafo británico',
             'pam': 'Computer scientist, mathematician, and cryptographer',
             'nl': 'Brits wiskundige',
             'de': 'britischer Logiker, Mathematiker und Kryptoanalytiker',
             'zh-cn': '英国数学家，逻辑学家，密码学家和计算机科学家',
             'en': 'British mathematician, logician, cryptanalyst, and '
                   'computer ' + 'scientist',
             'as': 'Computer scientist, mathematician, and cryptographer',
             'zh': '英国数学家，逻辑学家，密码学家和计算机科学家',
             'ru': 'английский математик, логик, криптограф',
             'pl': 'angielski matematyk',
             'sv': 'brittisk datavetare, matematiker och ingenjör',
             'es': 'matemático, filósofo y criptógrafo británico',
             'sk': 'britský matematik, logik, kryptograf a vojnový hrdina',
             'ilo': 'Britaniko a matematiko, lohiko, kriptoanalista, ken ' +
                'sientista ti kompiuter',
             'zh-hans': '英国数学家，逻辑学家，密码学家和计算机科学家',
             'fa': 'دانشمند کامپیوتر، رمزشکن، منطق\u200cدان و ریاضی' +
             '\u200cدان بریتانیایی',
             'nb': 'britisk informatiker, matematiker og ingeniør'})
    assert solve(revision.reference_claims, cache={r_text: ALAN_TEXT}) == 56
    assert (solve(revision.datasources.reference_claims,
            cache={r_text: ALAN_TEXT}) ==
            {('P108', 'Q220798', 'P248', 0, 'Q20895922'),
             ('P106', 'Q4964182', 'P143', 0, 'Q48952'),
             ('P69', 'Q924289', 'P248', 0, 'Q20895922'),
             ('P570', '+1954-06-07T00:00:00Z', 'P143', 0, 'Q206855'),
             ('P31', 'Q5', 'P248', 0, 'Q20666306'),
             ('P800', 'Q20895949', 'P248', 0, 'Q20895922'),
             ('P25', 'Q20895935', 'P248', 0, 'Q20895922'),
             ('P349', "'00621580'", 'P143', 0, 'Q48183'),
             ('P549', "'8014'", 'P143', 0, 'Q328'),
             ('P569', '+1912-06-23T00:00:00Z', 'P854', 0,
              "'http://data.bnf.fr/ark:/12148/cb12205670t'"),
             ('P18', "'Alan Turing Aged 16.jpg'", 'P143', 0, 'Q11920'),
             ('P569', '+1912-06-23T00:00:00Z', 'P248', 0, 'Q20666306'),
             ('P19', 'Q122744', 'P143', 0, 'Q328'),
             ('P214', "'41887917'", 'P143', 0, 'Q8447'),
             ('P569', '+1912-06-23T00:00:00Z', 'P143', 0, 'Q328'),
             ('P569', '+1912-06-23T00:00:00Z', 'P345', 0, "'nm6290133'"),
             ('P91', 'Q6636', 'P248', 0, 'Q20895922'),
             ('P1273', "'a11455408'", 'P854', 0,
              "'https://viaf.org/viaf/41887917/'"),
             ('P1412', 'Q1860', 'P143', 0, 'Q20666306'),
             ('P69', 'Q2278254', 'P248', 0, 'Q20895922'),
             ('P31', 'Q5', 'P813', 0, '+2015-10-10T00:00:00Z'),
             ('P512', 'Q230899', 'P143', 0, 'Q8447'),
             ('P512', 'Q21578', 'P143', 0, 'Q8447'),
             ('P1412', 'Q1860', 'P813', 0, '+2015-10-10T00:00:00Z'),
             ('P1412', 'Q1860', 'P854', 0,
              "'http://data.bnf.fr/ark:/12148/cb12205670t'"),
             ('P535', "'12651680'", 'P143', 0, 'Q328'),
             ('P19', 'Q20895942', 'P248', 0, 'Q20895922'),
             ('P227', "'118802976'", 'P143', 0, 'Q1419226'),
             ('P570', '+1954-06-07T00:00:00Z', 'P248', 0, 'Q20666306'),
             ('P21', 'Q6581097', 'P143', 0, 'Q54919'),
             ('P800', 'Q20895966', 'P248', 0, 'Q20895922'),
             ('P935', "'Alan Turing'", 'P143', 0, 'Q191168'),
             ('P31', 'Q5', 'P143', 0, 'Q206855'),
             ('P21', 'Q6581097', 'P248', 0, 'Q36578'),
             ('P646', "'/m/0n00'", 'P248', 0, 'Q15241312'),
             ('P646', "'/m/0n00'", 'P577', 0, '+2013-10-28T00:00:00Z'),
             ('P1563', "'Turing'", 'P143', 0, 'Q11921'),
             ('P19', 'Q122744', 'P854', 0,
              "'http://www.telegraph.co.uk/technology/news/9314910/Britain-still-owes-Alan-Turing-a-debt.html'"), # noqa
             ('P269', "'030691621'", 'P143', 0, 'Q8447'),
             ('P108', 'Q230899', 'P248', 0, 'Q20895922'),
             ('P22', 'Q20895930', 'P248', 0, 'Q20895922'),
             ('P906', "'254262'", 'P143', 0, 'Q877583'),
             ('P21', 'Q6581097', 'P813', 0, '+2014-04-09T00:00:00Z'),
             ('P244', "'n83171546'", 'P143', 0, 'Q328'),
             ('P570', '+1954-06-07T00:00:00Z', 'P854', 0,
              "'http://data.bnf.fr/ark:/12148/cb12205670t'"),
             ('P570', '+1954-06-07T00:00:00Z', 'P813', 0,
              '+2015-10-10T00:00:00Z'),
             ('P106', 'Q82594', 'P143', 0, 'Q328'),
             ('P570', '+1954-06-07T00:00:00Z', 'P345', 0, "'nm6290133'"),
             ('P213', "'0000 0001 1058 9902'", 'P143', 0, 'Q423048'),
             ('P31', 'Q5', 'P854', 0,
              "'http://data.bnf.fr/ark:/12148/cb12205670t'"),
             ('P569', '+1912-06-23T00:00:00Z', 'P813', 0,
              '+2015-10-10T00:00:00Z'),
             ('P1196', 'Q10737', 'P248', 0, 'Q20895922'),
             ('P268', "'12205670t'", 'P143', 0, 'Q8447'),
             ('P800', 'Q772056', 'P248', 0, 'Q20895922'),
             ('P20', 'Q2011497', 'P248', 0, 'Q20895922'),
             ('P27', 'Q145', 'P143', 0, 'Q48183')})


def test_has_property():
    assert solve(has_p106, cache={r_text: ALAN_TEXT})
    assert not solve(has_p999, cache={r_text: ALAN_TEXT})

    assert pickle.loads(pickle.dumps(has_p106)) == has_p106
    assert pickle.loads(pickle.dumps(has_p999)) == has_p999


def test_has_property_value():
    assert solve(has_p106_q82594, cache={r_text: ALAN_TEXT})
    assert not solve(has_p106_test, cache={r_text: ALAN_TEXT})
    assert not solve(has_p999_foo, cache={r_text: ALAN_TEXT})

    assert pickle.loads(pickle.dumps(has_p106_q82594)) == has_p106_q82594
    assert pickle.loads(pickle.dumps(has_p106_test)) == has_p106_test
    assert pickle.loads(pickle.dumps(has_p999_foo)) == has_p999_foo
