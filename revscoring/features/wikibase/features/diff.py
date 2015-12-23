import re

from ...feature import Feature
from ...meta import aggregators, bools


class Diff():

    def __init__(self, prefix, datasources):
        self.prefix = prefix
        self.datasources = datasources

        # Sitelinks
        self.sitelinks_added = \
            aggregators.len(self.datasources.sitelinks_added)
        self.sitelinks_removed = \
            aggregators.len(self.datasources.sitelinks_removed)
        self.sitelinks_changed = \
            aggregators.len(self.datasources.sitelinks_changed)

        # Labels
        self.labels_added = aggregators.len(self.datasources.labels_added)
        self.labels_removed = aggregators.len(self.datasources.labels_removed)
        self.labels_changed = aggregators.len(self.datasources.labels_changed)

        # Aliases
        self.aliases_added = aggregators.len(self.datasources.aliases_added)
        self.aliases_removed = \
            aggregators.len(self.datasources.aliases_removed)
        self.aliases_changed = \
            aggregators.len(self.datasources.aliases_changed)

        # Descriptions
        self.descriptions_added = \
            aggregators.len(self.datasources.descriptions_added)
        self.descriptions_removed = \
            aggregators.len(self.datasources.descriptions_removed)
        self.descriptions_changed = \
            aggregators.len(self.datasources.descriptions_changed)

        # Properties
        self.properties_added = \
            aggregators.len(self.datasources.properties_added)
        self.properties_removed = \
            aggregators.len(self.datasources.properties_removed)
        self.properties_changed = \
            aggregators.len(self.datasources.properties_changed)

        # Claims
        self.claims_added = \
            aggregators.len(self.datasources.claims_added)
        self.claims_removed = \
            aggregators.len(self.datasources.claims_removed)
        self.claims_changed = \
            aggregators.len(self.datasources.claims_changed)

        # Sources
        self.sources_added = aggregators.len(self.datasources.sources_added)
        self.sources_removed = \
            aggregators.len(self.datasources.sources_removed)

        # Qualifiers
        self.qualifiers_added = \
            aggregators.len(self.datasources.qualifiers_added)
        self.qualifiers_removed = \
            aggregators.len(self.datasources.qualifiers_removed)

        # Badges
        self.badges_added = aggregators.len(self.datasources.badges_added)
        self.badges_removed = aggregators.len(self.datasources.badges_removed)
        self.badges_changed = aggregators.len(self.datasources.badges_changed)

        # AF/38
        self.proportion_of_qid_added = Feature(
            prefix + ".proportion_of_qid_added",
            _process_proportion_of_qid_added,
            returns=float, depends_on=[self.datasources.parent_item,
                                       self.datasources.revision_item]
        )

        # AF/38
        self.proportion_of_language_added = Feature(
            prefix + ".proportion_of_language_added",
            _process_proportion_of_language_added,
            returns=float, depends_on=[self.datasources.parent_item,
                                       self.datasources.revision_item]
        )

        self.proportion_of_links_added = Feature(
            "proportion_of_links_added", _process_proportion_of_links_added,
            returns=float, depends_on=[self.datasources.parent_item,
                                       self.datasources.revision_item]
        )

    def property_changed(self, property, name=None):
        """
        Returns a :class:`revscoring.Feature` that represents whether a
        property was changed.

        :Parameters:
            property : `str`
                The property name
            name : `str`
                A name to associate with the feature.  If not set, the
                feature's name will be 'property_changed(<property>)'
        """
        if name is None:
            name = self.prefix + ".property_changed({0})" \
                                 .format(repr(property))
        return bools.item_in_set(property, self.datasources.properties_changed,
                                 name=name)


def _process_proportion_of_qid_added(parent_item, revision_item):
    parent_item_doc = parent_item.toJSON() if parent_item is not None else {}
    re_qid = re.compile(r'Q\d{1,8}')
    revision_item_qids = len(re.findall(re_qid, str(revision_item.toJSON())))
    parent_item_qids = len(re.findall(re_qid, str(parent_item_doc)))
    return float(revision_item_qids - parent_item_qids) / \
           float(revision_item_qids + 1)


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


def _process_proportion_of_language_added(parent_item, revision_item):
    parent_item_doc = parent_item.toJSON() if parent_item is not None else {}
    revision_item_res = len(re.findall(LANGUAGE_RE, str(revision_item.toJSON())))
    parent_item_res = len(re.findall(LANGUAGE_RE, str(parent_item_doc)))
    return float(revision_item_res - parent_item_res) / \
        float(revision_item_res + 1)


def _process_proportion_of_links_added(parent_item, revision_item):
    parent_item_doc = parent_item.toJSON() if parent_item is not None else {}
    re_qid = re.compile(r'https?\://|wwww\.')
    revision_item_res = len(re.findall(re_qid, str(revision_item.toJSON())))
    parent_item_res = len(re.findall(re_qid, str(parent_item_doc)))
    return float(revision_item_res - parent_item_res) / \
        float(revision_item_res + 1)
