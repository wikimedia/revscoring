import os
import pickle

from nose.tools import eq_

from ....datasources import revision_oriented
from ....dependencies import solve
from ..revision_oriented import revision

pwd = os.path.dirname(os.path.realpath(__file__))
ALAN_TEXT = open(os.path.join(pwd, "alan_turing.json")).read()

r_text = revision_oriented.revision.text

has_p106 = revision.has_property('P106')
has_p999 = revision.has_property('P999')

has_p106_q82594 = revision.has_property_value('P106', "Q82594")
has_p106_test = revision.has_property_value('P106', "Test")
has_p999_foo = revision.has_property_value('P999', "Foo")


def test_item_doc():
    solve(revision.datasources.item_doc, cache={r_text: ALAN_TEXT})
    eq_(solve(revision.datasources.item_doc, cache={r_text: None}), None)

    eq_(pickle.loads(pickle.dumps(revision.datasources.item_doc)),
        revision.datasources.item_doc)


def test_item():
    eq_(solve(revision.datasources.item, cache={r_text: None}).claims, {})

    solve(revision.datasources.item, cache={r_text: ALAN_TEXT})

    eq_(pickle.loads(pickle.dumps(revision.datasources.item)),
        revision.datasources.item)

    eq_(solve(revision.properties, cache={r_text: ALAN_TEXT}), 57)
    eq_(solve(revision.datasources.properties,
              cache={r_text: ALAN_TEXT}).keys(),
        {'P1430', 'P906', 'P1816', 'P570', 'P31', 'P1343', 'P2021', 'P535',
         'P800', 'P569', 'P373', 'P1819', 'P108', 'P227', 'P185', 'P910',
         'P1273', 'P69', 'P244', 'P20', 'P101', 'P106', 'P18', 'P1563', 'P25',
         'P646', 'P1296', 'P214', 'P950', 'P463', 'P1006', 'P268', 'P21',
         'P1417', 'P22', 'P1207', 'P19', 'P91', 'P735', 'P1412', 'P166',
         'P269', 'P1741', 'P1196', 'P27', 'P140', 'P512', 'P1415', 'P691',
         'P345', 'P949', 'P1263', 'P549', 'P184', 'P935', 'P349', 'P213'})

    eq_(solve(revision.claims, cache={r_text: ALAN_TEXT}), 71)
    eq_(solve(revision.datasources.claims, cache={r_text: ALAN_TEXT}),
        {('P646', '/m/0n00'), ('P101', 'Q897511'), ('P20', 'Q2011497'),
         ('P166', 'Q10762848'), ('P800', 'Q20895949'), ('P950', 'XX945020'),
         ('P1816', 'mp18700'), ('P1563', 'Turing'),
         ('P569', '+1912-06-23T00:00:00Z'), ('P19', 'Q122744'),
         ('P691', 'jn19990008646'), ('P185', 'Q249984'), ('P1343', 'Q2627728'),
         ('P512', 'Q21578'), ('P69', 'Q2278254'), ('P101', 'Q21198'),
         ('P800', 'Q772056'), ('P108', 'Q230899'), ('P25', 'Q20895935'),
         ('P1263', '952/000023883'), ('P214', '41887917'),
         ('P1296', '0067958'), ('P106', 'Q82594'), ('P106', 'Q4964182'),
         ('P1273', 'a11455408'), ('P1412', 'Q1860'), ('P1207', 'n98045497'),
         ('P910', 'Q9384007'), ('P140', 'Q7066'), ('P1430', '368'),
         ('P69', 'Q924289'),
         ('P2021', 'WbQuantity(amount=5, upperBound=5, lowerBound=5, unit=1)'),
         ('P463', 'Q123885'), ('P166', 'Q15631401'),
         ('P373', 'Alan Turing'), ('P549', '8014'),
         ('P213', '0000 0001 1058 9902'), ('P1417', '609739'),
         ('P27', 'Q145'), ('P21', 'Q6581097'), ('P268', '12205670t'),
         ('P184', 'Q92741'), ('P1196', 'Q10737'), ('P244', 'n83171546'),
         ('P22', 'Q20895930'), ('P269', '030691621'), ('P1741', '226316'),
         ('P106', 'Q81096'), ('P935', 'Alan Turing'), ('P1006', '070580685'),
         ('P69', 'Q21578'), ('P227', '118802976'), ('P906', '254262'),
         ('P349', '00621580'), ('P535', '12651680'), ('P91', 'Q6636'),
         ('P106', 'Q11513337'), ('P345', 'nm6290133'), ('P31', 'Q5'),
         ('P570', '+1954-06-07T00:00:00Z'), ('P18', 'Alan Turing Aged 16.jpg'),
         ('P735', 'Q294833'), ('P512', 'Q230899'), ('P1343', 'Q17329836'),
         ('P1415', '101036578'), ('P106', 'Q170790'), ('P1819', 'I00586443'),
         ('P949', '000133188'), ('P19', 'Q20895942'), ('P800', 'Q20895966'),
         ('P108', 'Q220798')})
    eq_(solve(revision.aliases, cache={r_text: ALAN_TEXT}), 9)
    eq_(solve(revision.datasources.aliases, cache={r_text: ALAN_TEXT}),
        {'de': ['Alan Mathison Turing'], 'en': ['Alan Mathison Turing'],
         'fr': ['Alan Mathison Turing'], 'ru': ['Тьюринг, Алан'],
         'jbo': ['alan turin'], 'it': ['Alan Mathison Turing'],
         'ko': ['앨런 매티슨 튜링'],
         'be-tarask': ["Элан Т'юрынг", 'Алан Цюрынг', "Т'юрынг"],
         'ja': ['アラン・テューリング']})
    eq_(solve(revision.sources, cache={r_text: ALAN_TEXT}), 53)
    eq_(solve(revision.datasources.sources, cache={r_text: ALAN_TEXT}),
        {('P19', 'Q122744', 0), ('P570', '+1954-06-07T00:00:00Z', 1),
         ('P19', 'Q122744', 1), ('P570', '+1954-06-07T00:00:00Z', 2),
         ('P570', '+1954-06-07T00:00:00Z', 3), ('P535', '12651680', 0),
         ('P108', 'Q220798', 0), ('P214', '41887917', 0),
         ('P906', '254262', 0), ('P1273', 'a11455408', 0),
         ('P25', 'Q20895935', 0), ('P800', 'Q20895949', 0),
         ('P106', 'Q4964182', 0), ('P69', 'Q924289', 0),
         ('P214', '41887917', 1), ('P108', 'Q230899', 0),
         ('P21', 'Q6581097', 0), ('P18', 'Alan Turing Aged 16.jpg', 0),
         ('P269', '030691621', 0), ('P935', 'Alan Turing', 0),
         ('P214', '41887917', 2), ('P21', 'Q6581097', 1),
         ('P646', '/m/0n00', 0), ('P244', 'n83171546', 0),
         ('P244', 'n83171546', 1), ('P800', 'Q20895966', 0),
         ('P27', 'Q145', 0), ('P20', 'Q2011497', 0), ('P69', 'Q2278254', 0),
         ('P800', 'Q772056', 0), ('P1412', 'Q1860', 0), ('P106', 'Q82594', 0),
         ('P31', 'Q5', 2), ('P213', '0000 0001 1058 9902', 0),
         ('P569', '+1912-06-23T00:00:00Z', 3), ('P31', 'Q5', 1),
         ('P22', 'Q20895930', 0), ('P569', '+1912-06-23T00:00:00Z', 2),
         ('P227', '118802976', 1), ('P31', 'Q5', 0), ('P19', 'Q20895942', 0),
         ('P512', 'Q230899', 0), ('P512', 'Q21578', 0),
         ('P569', '+1912-06-23T00:00:00Z', 1), ('P227', '118802976', 0),
         ('P349', '00621580', 0), ('P569', '+1912-06-23T00:00:00Z', 0),
         ('P549', '8014', 0), ('P1196', 'Q10737', 0), ('P91', 'Q6636', 0),
         ('P268', '12205670t', 0), ('P570', '+1954-06-07T00:00:00Z', 0),
         ('P1563', 'Turing', 0)})
    eq_(solve(revision.qualifiers, cache={r_text: ALAN_TEXT}), 6)
    eq_(solve(revision.datasources.qualifiers, cache={r_text: ALAN_TEXT}),
        {('P1343', 'Q17329836', 'P854'), ('P1343', 'Q2627728', 'P854'),
        ('P69', 'Q2278254', 'P580'), ('P108', 'Q220798', 'P582'),
        ('P108', 'Q220798', 'P580'), ('P108', 'Q230899', 'P580')})
    eq_(solve(revision.badges, cache={r_text: ALAN_TEXT}), 5)
    eq_(solve(revision.datasources.badges, cache={r_text: ALAN_TEXT}),
        {'aswiki': ['Q17437798'], 'ruwiki': ['Q17437798'],
         'azwiki': ['Q17437796'], 'lawiki': ['Q17437796'],
         'enwiki': ['Q17437798']})
    eq_(solve(revision.labels, cache={r_text: ALAN_TEXT}), 126)
    eq_(solve(revision.datasources.labels, cache={r_text: ALAN_TEXT}),
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
         'new': 'एलेन त्युरिङ्ग', 'tt': 'Alan Tyuring', 'ht': 'Alan Turing',
         'cy': 'Alan Turing', 'mwl': 'Alan Turing', 'or': 'ଆଲାନ ଟ୍ୟୁରିଙ୍ଗ',
         'jbo': '.alan turin', 'ml': 'അലൻ ട്യൂറിംഗ്', 'sa': 'एलेन ट्यूरिंग',
         'bs': 'Alan Turing', 'tg': 'Алан Тюринг', 'ms': 'Alan Turing',
         'lv': 'Alans Tjūrings', 'fur': 'Alan Turing', 'sco': 'Alan Turing',
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
    eq_(solve(revision.sitelinks, cache={r_text: ALAN_TEXT}), 134)
    eq_(solve(revision.datasources.sitelinks, cache={r_text: ALAN_TEXT}),
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
         'ganwiki': '圖靈', 'ckbwiki': 'ئالان تیورینگ', 'slwiki': 'Alan Turing'})
    eq_(solve(revision.descriptions, cache={r_text: ALAN_TEXT}), 22)
    eq_(solve(revision.datasources.descriptions, cache={r_text: ALAN_TEXT}),
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
         'en': 'British mathematician, logician, cryptanalyst, and computer ' +
               'scientist',
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


def test_has_property():
    assert solve(has_p106, cache={r_text: ALAN_TEXT})
    assert not solve(has_p999, cache={r_text: ALAN_TEXT})

    eq_(pickle.loads(pickle.dumps(has_p106)), has_p106)
    eq_(pickle.loads(pickle.dumps(has_p999)), has_p999)


def test_has_property_value():
    assert solve(has_p106_q82594, cache={r_text: ALAN_TEXT})
    assert not solve(has_p106_test, cache={r_text: ALAN_TEXT})
    assert not solve(has_p999_foo, cache={r_text: ALAN_TEXT})

    eq_(pickle.loads(pickle.dumps(has_p106_q82594)), has_p106_q82594)
    eq_(pickle.loads(pickle.dumps(has_p106_test)), has_p106_test)
    eq_(pickle.loads(pickle.dumps(has_p999_foo)), has_p999_foo)
