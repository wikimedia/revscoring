import pickle

from nose.tools import eq_

from .. import korean
from ...datasources import revision_oriented
from ...dependencies import solve
from .util import compare_extraction

BAD = [
    'ㅂㅅ',
    'ㅅㅂ',
    'ㅆㅂ',
    'ㅈㄹ',
    '간나',
    '갈보',
    '개기다', '개기지', '개년', '개새끼', '개소리', '개수작', '개자식', '개좆', '개좆', '개차반',
    '걸레년',
    '계집년',
    '그지새끼',
    '꼴값',
    '눈깔',
    '느금마',
    '대가리', '대갈빡',
    '뒈져라', '뒤져', '뒤져라', '디져라',
    '또라이',
    '띠발',
    '미친놈',
    '버러지년',
    '병시나', '병신',
    '븅신',
    '빌어먹을',
    '빙신',
    '빡대갈',
    '뻐큐',
    '색히',
    '시부랄',
    '쌍년', '쌍놈',
    '썅', '썅년', '썅놈',
    '쓰레기같은', '쓰벌',
    '씨바', '씨발', '씨발년', '씨발놈',
    '씹구멍', '씹물', '씹버러지', '씹빨', '씹새', '씹알', '씹창',
    '아가리',
    '애자',
    '앰창', '엠창',
    '염병', '옘병',
    '잡년',
    '조빱',
    '존나',
    '좆같', '좆까', '좆나', '좆만한', '좆밥', '좆빠는', '좆뺑이', '좆씹',
    '지랄',
    '찌질이',
    '찐따',
    '창년',
    '처먹다', '쳐먹다',
    '호로자식',
    '화냥',
    '후레'
]

INFORMAL = [
    "아니오"
    "잠시만요"
    "합니다만", "입니다만"
    "알겠습니다", "죄송합니다", "그렇습니다", "모르겠습니까"
    "식사하세요", "그러세요", "모르세요", "해보세요"
    "이건데요", "있는데요",
    "이거지요", "이상하지요", "됐지요"
    "됐네요", "쐈네요",
    "알겠어요", "됐어요",
    "하죠"
]


OTHER = [
    """
    요하네스 케플러(Johannes Kepler, 1571년 12월 27일 - 1630년 11월 15일)는
    독일의 수학자, 천문학자, 점성술사로, 17세기 천문학 혁명의 중심 인물이었다. 그는 자신의
    이름이 붙은 행성운동법칙으로 유명하며, 후대의 천문학자들은 그의 저작 《신천문학》,
    《우주의 조화》, 그리고 《코페르니쿠스 천문학 개요》를 바탕으로 그 법칙을 성문화하였다.
    또한 이 저작들은 아이작 뉴턴이 만유인력의 법칙을 확립하는 데 기초를 제공하였다.
    생애 동안 케플러는 오스트리아 그라츠 신학교의 수학 선생, 천문학자 튀코 브라헤의
    조수, 루돌프 2세·마티아스·페르디난트 2세의 세 황제를 모신 신성 로마 제국의 제국
    수학자, 오스트리아 린츠에서의 수학 선생, 발렌슈타인 장군의 점성술사라는 다양한 경력의
    소유자였다. 또한 그는 광학 연구 분야의 초석을 닦았으며, 굴절 망원경을 개조하여
    성능을 향상시켰으며(케플러식 망원경), 동시대의 인물인 갈릴레오 갈릴레이의 망원경을
    이용한 발견이 공식적으로 인정되는 데 공헌하였다.
    """,
]

r_text = revision_oriented.revision.text


def test_badwords():
    compare_extraction(korean.badwords.revision.datasources.matches,
                       BAD, OTHER)

    eq_(korean.badwords, pickle.loads(pickle.dumps(korean.badwords)))


def test_informals():
    compare_extraction(korean.informals.revision.datasources.matches,
                       INFORMAL, OTHER)

    eq_(korean.informals, pickle.loads(pickle.dumps(korean.informals)))
