import sys

from .space_delimited import SpaceDelimited

try:
    import enchant
    dictionary = enchant.Dict("vi")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'vi'.  " +
                      "Consider installing 'hunspell-vi'.")

# https://vi.wiktionary.org/wiki/Th%C3%A0nh_vi%C3%AAn:Laurent_Bouvier/
# Free_Vietnamese_Dictionary_Project_Vietnamese-Vietnamese#Allwiki_.28closed.29
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
    # Vietnamese
    r"[ck]ặ[tc]", r"[ck]u", r"cứt", r"(dz?|gi)âm", r"đái", r"đéo", r"đ[ụù]",
    r"đĩ", r"đ[íị]t", r"ỉa", r"l[ôồ]n", r"trứng"
]
informals = [
    # Vietnamese
    r"bợn", r"bro",
    r"chẳng", r"ch[ớứ]", r"cú",
    r"đụ", r"đừng", r"fải",
    r"khỉ",
    r"mày", r"nghịch", r"ngu", r"ngụy", r"nguỵ",
    r"ok", r"ơi",
    r"quái",
    r"thằng", r"thôi", r"tui", r"ừ", r"vời", r"wái?",
    r"zì"
]

sys.modules[__name__] = SpaceDelimited(
    __name__,
    doc="""
vietnamese
==========

revision
--------
.. autoattribute:: revision.words
.. autoattribute:: revision.content_words
.. autoattribute:: revision.badwords
.. autoattribute:: revision.misspellings
.. autoattribute:: revision.informals

parent_revision
---------------
.. autoattribute:: parent_revision.words
.. autoattribute:: parent_revision.content_words
.. autoattribute:: parent_revision.badwords
.. autoattribute:: parent_revision.misspellings
.. autoattribute:: parent_revision.informals

diff
----
.. autoattribute:: diff.words_added
.. autoattribute:: diff.words_removed
.. autoattribute:: diff.badwords_added
.. autoattribute:: diff.badwords_removed
.. autoattribute:: diff.informals_added
.. autoattribute:: diff.informals_removed
.. autoattribute:: diff.misspellings_added
.. autoattribute:: diff.misspellings_removed
    """,
    badwords=badwords,
    dictionary=dictionary,
    informals=informals,
    stopwords=stopwords
)
"""
vietnamese
----------
"""
