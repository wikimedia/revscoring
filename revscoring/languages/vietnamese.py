import re
import warnings

import enchant

from .language import Language, LanguageUtility

# https://vi.wiktionary.org/wiki/Th%C3%A0nh_vi%C3%AAn:Laurent_Bouvier/Free_Vietnamese_Dictionary_Project_Vietnamese-Vietnamese#Allwiki_.28closed.29
STOPWORDS = set([
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
BAD_REGEXES = [
    "[ck]ặ[tc]", "[ck]u", "cứt", "(dz?|gi)âm", "đái", "đéo", "đ[ụù].", "đĩ",
    "đ[íị]t", "ỉa", "l[ôồ]n",
    "dick", "cunt", "fag", "bitch", "shit", "fuck.*", "ass", "gay", "ghey",
    "slut",
]
INFORMAL_REGEXES = [
    "bợn", "bro", "chẳng", "ch[ớứ]", "cú", "đừng", "fải", "(he){2,}", "(hi)+",
    "khỉ", "mày", "nghịch", "ngu", "ngụy", "nguỵ", "ok", "ơi", "quái", "thằng",
    "thôi", "tui", "ừ", "vời", "wái?", "zì",
    "moron", "retard", "stupid",
]
BAD_REGEX = re.compile("|".join(BAD_REGEXES))
INFORMAL_REGEX = re.compile("|".join(INFORMAL_REGEXES))
DICTIONARY = enchant.Dict("vi")

def stem_word_process():
    def stem_word(word):
        return word.lower()
    return stem_word
stem_word = LanguageUtility("stem_word", stem_word_process)

def is_badword_process():
    def is_badword(word):
        return bool(BAD_REGEX.match(word.lower()))
    return is_badword
is_badword = LanguageUtility("is_badword", is_badword_process)

def is_informal_word_process():
    def is_informal_word(word):
        return bool(INFORMAL_REGEX.match(word.lower()))
    return is_informal_word
is_informal_word = LanguageUtility("is_informal_word",
    is_informal_word_process, depends_on=[])

def is_misspelled_process():
    def is_misspelled(word):
        return not DICTIONARY.check(word)
    return is_misspelled

is_misspelled = LanguageUtility("is_misspelled", is_misspelled_process)

def is_stopword_process():
    def is_stopword(word):
        return word.lower() in STOPWORDS
    return is_stopword
is_stopword = LanguageUtility("is_stopword", is_stopword_process)

vietnamese = Language("revscoring.languages.vietnamese",
                      [stem_word, is_badword, is_informal_word, is_misspelled,
                       is_stopword])
