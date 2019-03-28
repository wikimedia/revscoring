import re

import mwbase

from revscoring.dependencies import DependentSet

from ...feature import Feature
from ...meta import aggregators, bools


class Diff(DependentSet):

    def __init__(self, name, datasources):
        super().__init__(name)
        self.datasources = datasources

        # Sitelinks
        self.sitelinks_added = \
            aggregators.len(self.datasources.sitelinks_added)
        "`int` : The number of sitelinks added"
        self.sitelinks_removed = \
            aggregators.len(self.datasources.sitelinks_removed)
        "`int` : The number of sitelinks removed"
        self.sitelinks_changed = \
            aggregators.len(self.datasources.sitelinks_changed)
        "`int` : The number of sitelinks changed"

        # Labels
        self.labels_added = aggregators.len(self.datasources.labels_added)
        "`int` : The number of labels added"
        self.labels_removed = aggregators.len(self.datasources.labels_removed)
        "`int` : The number of labels removed"
        self.labels_changed = aggregators.len(self.datasources.labels_changed)
        "`int` : The number of labels changed"

        # Aliases
        self.aliases_added = aggregators.len(self.datasources.aliases_added)
        "`int` : The number of aliases added"
        self.aliases_removed = \
            aggregators.len(self.datasources.aliases_removed)
        "`int` : The number of aliases removed"
        self.aliases_changed = \
            aggregators.len(self.datasources.aliases_changed)
        "`int` : The number of aliases changed"

        # Descriptions
        self.descriptions_added = \
            aggregators.len(self.datasources.descriptions_added)
        "`int` : The number of descriptions added"
        self.descriptions_removed = \
            aggregators.len(self.datasources.descriptions_removed)
        "`int` : The number of descriptions removed"
        self.descriptions_changed = \
            aggregators.len(self.datasources.descriptions_changed)
        "`int` : The number of descriptions changed"

        # Properties
        self.properties_added = \
            aggregators.len(self.datasources.properties_added)
        "`int` : The number of properties added"
        self.properties_removed = \
            aggregators.len(self.datasources.properties_removed)
        "`int` : The number of properties removed"
        self.properties_changed = \
            aggregators.len(self.datasources.properties_changed)
        "`int` : The number of properties changed"

        # Claims
        self.statements_added = \
            aggregators.len(self.datasources.statements_added)
        "`int` : The number of statements/claims added"
        self.claims_added = \
            aggregators.len(self.datasources.claims_added)  # Backwards compatible
        "`int` : The number of statements/claims added"
        self.statements_removed = \
            aggregators.len(self.datasources.statements_removed)
        "`int` : The number of statements/claims removed"
        self.claims_removed = \
            aggregators.len(self.datasources.claims_removed)  # Backwards compatible
        "`int` : The number of statements/claims removed"
        self.statements_changed = \
            aggregators.len(self.datasources.statements_changed)
        "`int` : The number of statements/claims changed"
        self.claims_changed = \
            aggregators.len(self.datasources.claims_changed)  # Backwards compatible
        "`int` : The number of statements/claims changed"

        # Sources
        self.sources_added = aggregators.len(self.datasources.sources_added)
        "`int` : The number of sources added"
        self.sources_removed = \
            aggregators.len(self.datasources.sources_removed)
        "`int` : The number of sources removed"

        # Qualifiers
        self.qualifiers_added = \
            aggregators.len(self.datasources.qualifiers_added)
        "`int` : The number of qualifiers added"
        self.qualifiers_removed = \
            aggregators.len(self.datasources.qualifiers_removed)
        "`int` : The number of qualifiers removed"

        # Badges
        self.badges_added = aggregators.len(self.datasources.badges_added)
        "`int` : The number of badges added"
        self.badges_removed = aggregators.len(self.datasources.badges_removed)
        "`int` : The number of badges removed"
        self.badges_changed = aggregators.len(self.datasources.badges_changed)
        "`int` : The number of badges changed"

        # AF/38
        self.proportion_of_qid_added = Feature(
            name + ".proportion_of_qid_added",
            _process_proportion_of_qid_added,
            returns=float, depends_on=[self.datasources.parent_entity,
                                       self.datasources.revision_entity]
        )
        "`int` : The proportion of Q# added."

        # AF/38
        self.proportion_of_language_added = Feature(
            name + ".proportion_of_language_added",
            _process_proportion_of_language_added,
            returns=float, depends_on=[self.datasources.parent_entity,
                                       self.datasources.revision_entity]
        )
        "`int` : The proportion of language added."

        self.proportion_of_links_added = Feature(
            name + ".proportion_of_links_added",
            _process_proportion_of_links_added,
            returns=float, depends_on=[self.datasources.parent_entity,
                                       self.datasources.revision_entity]
        )
        "`int` : The proportion of links added."

        self.identifiers_changed = Feature(
            name + ".identifiers_changed",
            _process_identifiers_changed,
            returns=int, depends_on=[self.datasources.claims_changed]
        )
        "`int` : The number of identifiers that were changed"

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
            name = self._name + ".property_changed({0})" \
                .format(repr(property))
        return bools.item_in_set(property, self.datasources.properties_changed,
                                 name=name)


def _process_proportion_of_qid_added(parent_entity, revision_entity):
    parent_entity_doc = parent_entity if parent_entity is not None else {}
    re_qid = re.compile(r'Q\d{1,8}')
    revision_entity_qids = len(re.findall(
        re_qid, mwbase.json_dumps(revision_entity)))
    parent_entity_qids = len(re.findall(
        re_qid, mwbase.json_dumps(parent_entity_doc)))
    return float(revision_entity_qids - parent_entity_qids) / \
        float(revision_entity_qids + 1)


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


def _process_proportion_of_language_added(parent_entity, revision_entity):
    parent_entity_doc = parent_entity if parent_entity is not None else {}
    revision_entity_res = len(re.findall(LANGUAGE_RE,
                                         mwbase.json_dumps(revision_entity)))
    parent_entity_res = len(re.findall(LANGUAGE_RE,
                                       mwbase.json_dumps(parent_entity_doc)))
    return float(revision_entity_res - parent_entity_res) / \
        float(revision_entity_res + 1)


def _process_proportion_of_links_added(parent_entity, revision_entity):
    parent_entity_doc = parent_entity if parent_entity is not None else {}
    re_qid = re.compile(r'https?\://|wwww\.')
    revision_entity_res = len(re.findall(re_qid,
                                         mwbase.json_dumps(revision_entity)))
    parent_entity_res = len(re.findall(re_qid,
                                       mwbase.json_dumps(parent_entity_doc)))
    return float(revision_entity_res - parent_entity_res) / \
        float(revision_entity_res + 1)


def _process_identifiers_changed(changed_claims):
    counter = 0
    for old, new in changed_claims:
        if isinstance(old.claim.datavalue, mwbase.String):
            counter += 1
    return counter
