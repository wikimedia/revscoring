import re
import sys

import enchant

from .language import RegexLanguage

# https://vi.wiktionary.org/wiki/Th%C3%A0nh_vi%C3%AAn:Laurent_Bouvier/Free_Vietnamese_Dictionary_Project_Vietnamese-Vietnamese#Allwiki_.28closed.29
stopwords = set([
    "ai", "bằng", "bị", "bộ", "cho", "chưa", "chỉ", "cuối", "cuộc",
    "các", "cách", "cái", "có", "cùng", "cũng", "cạnh", "cả", "cục",
    "của", "dùng", "dưới", "dừng", "giữa", "gì", "hay", "hoặc",
    "khi", "khác", "không", "luôn", "là", "làm", "lại", "mà", "mọi",
    "mỗi", "một", "nhiều", "như", "nhưng", "nào", "này", "nữa",
    "phải", "qua", "quanh", "quá", "ra", "rất", "sau", "sẽ", "sự",
    "theo", "thành", "thêm", "thì", "thứ", "trong", "trên", "trước",
    "trừ", "tuy", "tìm", "từng", "và", "vài", "vào", "vì", "vẫn",
    "về", "với", "xuống", "đang", "đã", "được", "đấy", "đầu", "đủ"
])
badwords = [
    "[ck]ặ[tc]", "[ck]u", "cứt", "(dz?|gi)âm", "đái", "đéo", "đ[ụù].", "đĩ",
    "đ[íị]t", "ỉa", "l[ôồ]n",
    "dick", "cunt", "fag", "bitch", "shit", "fuck.*", "ass", "gay", "ghey",
    "slut",
]
informals = [
    "bợn", "bro", "chẳng", "ch[ớứ]", "cú", "đừng", "fải", "(he){2,}", "(hi)+",
    "khỉ", "mày", "nghịch", "ngu", "ngụy", "nguỵ", "ok", "ơi", "quái", "thằng",
    "thôi", "tui", "ừ", "vời", "wái?", "zì",
    "moron", "retard", "stupid",
]

try:
    dictionary = enchant.Dict("vi")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'vi'.  " +
                      "Consider installing 'hunspell-vi'.")

sys.modules[__name__] = RegexLanguage(
    __name__,
    badwords=badwords,
    informals=informals,
    stopwords=stopwords,
    dictionary=dictionary
)
"""
Implements :class:`~revscoring.languages.language.RegexLanguage` for Vietnamese.
:data:`~revscoring.languages.language.is_badword`,
:data:`~revscoring.languages.language.is_informal_word` and
:data:`~revscoring.languages.language.is_stopword` are provided.
"""
