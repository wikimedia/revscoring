from .features import Dictionary, RegexMatches, Stopwords

name = "vietnamese"

try:
    import enchant
    dictionary = enchant.Dict("vi")
except enchant.errors.DictNotFoundError:
    raise ImportError("No enchant-compatible dictionary found for 'vi'.  " +
                      "Consider installing 'hunspell-vi'.")

dictionary = Dictionary(name + ".dictionary", dictionary.check)
"""
:class:`~revscoring.languages.features.Dictionary` features via
:class:`enchant.Dict` "vi". Provided by `hunspell-vi`.
"""

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

stopwords = Stopwords(name + ".stopwords", stopwords)
"""
:class:`~revscoring.languages.features.Stopwords` features copied from
https://vi.wiktionary.org/wiki/Th%C3%A0nh_vi%C3%AAn:Laurent_Bouvier/Free_Vietnamese_Dictionary_Project_Vietnamese-Vietnamese#Allwiki_.28closed.29
"""  # noqa

badword_regexes = [
    # Vietnamese
    r"[ck]ặ[tc]", r"[ck]u", r"cứt", r"(dz?|gi)âm", r"đái", r"đéo", r"đ[ụù]",
    r"đĩ", r"đ[íị]t", r"ỉa", r"l[ôồ]n", r"trứng"
]

badwords = RegexMatches(name + ".badwords", badword_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
badword detecting regexes.
"""

informal_regexes = [
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

informals = RegexMatches(name + ".informals", informal_regexes)
"""
:class:`~revscoring.languages.features.RegexMatches` features via a list of
informal word detecting regexes.
"""
