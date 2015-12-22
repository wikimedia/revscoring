import re

from . import datasources
from ...feature import Feature
from ...meta import aggregators

revision_item = datasources.revision_item
parent_item = datasources.parent_item

# Sitelinks
sitelinks_added = aggregators.len(datasources.sitelinks_added)
sitelinks_removed = aggregators.len(datasources.sitelinks_removed)
sitelinks_changed = aggregators.len(datasources.sitelinks_changed)

# Labels
labels_added = aggregators.len(datasources.labels_added)
labels_removed = aggregators.len(datasources.labels_removed)
labels_changed = aggregators.len(datasources.labels_changed)

# Aliases
aliases_added = aggregators.len(datasources.aliases_added)
aliases_removed = aggregators.len(datasources.aliases_removed)
aliases_changed = aggregators.len(datasources.aliases_changed)

# Descriptions
descriptions_added = aggregators.len(datasources.descriptions_added)
descriptions_removed = aggregators.len(datasources.descriptions_removed)
descriptions_changed = aggregators.len(datasources.descriptions_changed)

# Claims
claims_added = aggregators.len(datasources.claims_added)
claims_removed = aggregators.len(datasources.claims_removed)
claims_changed = aggregators.len(datasources.claims_changed)

# Sources
sources_added = aggregators.len(datasources.sources_added)
sources_removed = aggregators.len(datasources.sources_removed)

# Qualifiers
qualifiers_added = aggregators.len(datasources.qualifiers_added)
qualifiers_removed = aggregators.len(datasources.qualifiers_removed)

# Badges
badges_added = aggregators.len(datasources.badges_added)
badges_removed = aggregators.len(datasources.badges_removed)
badges_changed = aggregators.len(datasources.badges_changed)


class property_changed(Feature):
    """
    Returns True if a property has changed.

    :Parameters:
        property : `str`
            The property name
        name : `str`
            A name to associate with the feature.  If not set, the feature's
            name will be 'wikibase.diff.property_changed(<property>)'
    """
    def __init__(self, property, name=None):
        self.property = property
        if name is None:
            name = "wikibase.diff.property_changed({0})".format(repr(property))

        super().__init__(name, self.process, returns=bool,
                         depends_on=[datasources.claims_changed])

    def process(self, claims_changed):
        return self.property in [claims[0].id for claims in claims_changed]


def process_proportion_of_qid_added(parent_item, revision_item):
    parent_item_doc = parent_item.toJSON() if parent_item is not None else {}
    re_qid = re.compile(r'Q\d{1,8}')
    revision_item_qids = len(re.findall(re_qid, str(revision_item.toJSON())))
    parent_item_qids = len(re.findall(re_qid, str(parent_item_doc)))
    return float(revision_item_qids - parent_item_qids) / \
        float(revision_item_qids + 1)

# AF/38
proportion_of_qid_added = Feature(
    "proportion_of_qid_added", process_proportion_of_qid_added, returns=float,
    depends_on=[parent_item, revision_item])

# AF/8
LANGUAGE_REGEXES = (r"(a(frikaa?ns|lbanian?|lemanha|ng(lais|ol)|ra?b(e?|"
                    r"[ei]c|ian?|isc?h)|rmenian?|ssamese|azeri|z[eə]rba"
                    r"(ijani?|ycan(ca)?|yjan)|нглийский)|b(ahasa( (indonesia|"
                    r"jawa|malaysia|melayu))?|angla|as(k|qu)e|[aeo]ng[ao]?li|"
                    r"elarusian?|okmål|osanski|ra[sz]il(ian?)?|ritish( "
                    r"kannada)?|ulgarian?)|c(ebuano|hina|hinese( simplified)?"
                    r"|zech|roat([eo]|ian?)|atal[aà]n?|рпски|antonese)|[cč]"
                    r"(esky|e[sš]tina)|d(an(isc?h|sk)|e?uts?ch)|e(esti|ll[hi]"
                    r"nika|ng(els|le(ski|za)|lisc?h)|spa(g?[nñ]h?i?ol|nisc?h)"
                    r"|speranto|stonian|usk[ae]ra)|f(ilipino|innish|ran[cç]"
                    r"(ais|e|ez[ao])|ren[cs]h|arsi|rancese)|g(al(ego|ician)|"
                    r"uja?rati|ree(ce|k)|eorgian|erman[ay]?|ilaki)|h(ayeren|"
                    r"ebrew|indi|rvatski|ungar(y|ian))|i(celandic|ndian?|"
                    r"ndonesian?|ngl[eê]se?|ngilizce|tali(ano?|en(isch)?))|"
                    r"ja(pan(ese)?|vanese)|k(a(nn?ada|zakh)|hmer|o(rean?|"
                    r"sova)|urd[iî])|l(at(in[ao]?|vi(an?|e[sš]u))|ietuvi[uų]"
                    r"|ithuanian?)|m(a[ck]edon(ian?|ski)|agyar|alay(alam?|"
                    r"sian?)?|altese|andarin|arathi|elayu|ontenegro|ongol"
                    r"(ian?)|yanmar)|n(e(d|th)erlands?|epali|orw(ay|egian)|"
                    r"orsk( bokm[aå]l)?|ynorsk)|o(landese|dia)|p(ashto|"
                    r"ersi?an?|ol(n?isc?h|ski)|or?tugu?[eê]se?(( d[eo])? "
                    r"brasil(eiro)?| ?\(brasil\))?|unjabi)|r(om[aâi]ni?[aă]n?"
                    r"|um(ano|änisch)|ussi([ao]n?|sch))|s(anskrit|erbian|"
                    r"imple english|inha?la|lov(ak(ian?)?|enš?[cč]ina|"
                    r"en(e|ij?an?)|uomi)|erbisch|pagnolo?|panisc?h|rbeska|"
                    r"rpski|venska|c?wedisc?h|hqip)|t(a(galog|mil)|elugu|"
                    r"hai(land)?|i[eế]ng vi[eệ]t|[uü]rk([cç]e|isc?h|iş|ey))|"
                    r"u(rdu|zbek)|v(alencia(no?)?|ietnamese)|welsh|(англиис|"
                    r"[kк]алмыкс|[kк]азахс|немец|[pр]усс|[yу]збекс|"
                    r"татарс)кий( язык)??|עברית|[kкқ](аза[кқ]ша|ыргызча|"
                    r"ирилл)|українськ(а|ою)|б(еларуская|"
                    r"ългарски( език)?)|ελλ[ηι]"
                    r"νικ(ά|α)|ქართული|हिन्दी|ไทย|[mм]онгол(иа)?|([cс]рп|"
                    r"[mм]акедон)ски|العربية|日本語|한국(말|어)|‌हिनद़ि|"
                    r"বাংলা|ਪੰਜਾਬੀ|मराठी|ಕನ್ನಡ|اُردُو|தமிழ்|తెలుగు|ગુજરાતી|"
                    r"فارسی|پارسی|മലയാളം|پښتو|မြန်မာဘာသာ|中文(简体|繁體)?|"
                    r"中文（(简体?|繁體)）|简体|繁體)")
LANGUAGE_RE = re.compile(LANGUAGE_REGEXES)


def process_proportion_of_language_added(parent_item, revision_item):
    parent_item_doc = parent_item.toJSON() if parent_item is not None else {}
    revision_item_res = len(re.findall(LANGUAGE_RE, str(revision_item.toJSON())))
    parent_item_res = len(re.findall(LANGUAGE_RE, str(parent_item_doc)))
    return float(revision_item_res - parent_item_res) / \
        float(revision_item_res + 1)

# AF/38
proportion_of_language_added = Feature(
    "proportion_of_language_added", process_proportion_of_language_added,
    returns=float, depends_on=[parent_item, revision_item])


def process_proportion_of_links_added(parent_item, revision_item):
    parent_item_doc = parent_item.toJSON() if parent_item is not None else {}
    re_qid = re.compile(r'https?\://|wwww\.')
    revision_item_res = len(re.findall(re_qid, str(revision_item.toJSON())))
    parent_item_res = len(re.findall(re_qid, str(parent_item_doc)))
    return float(revision_item_res - parent_item_res) / \
        float(revision_item_res + 1)

proportion_of_links_added = Feature(
    "proportion_of_links_added", process_proportion_of_links_added,
    returns=float, depends_on=[parent_item, revision_item])
