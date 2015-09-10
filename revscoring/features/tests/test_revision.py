from collections import namedtuple

from mwtypes import Timestamp
from nose.tools import eq_

from ...datasources import revision
from ...dependencies import solve
from ..revision import (bytes, category_links, chars, cite_templates,
                        content_chars, day_of_week, has_custom_comment,
                        has_section_comment, hour_of_day, image_links,
                        infobox_templates, internal_links, level_1_headings,
                        level_2_headings, level_3_headings, level_4_headings,
                        level_5_headings, level_6_headings, markup_chars,
                        numeric_chars, ref_tags, symbolic_chars, templates,
                        uppercase_chars)


def test_day_of_week():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata", ['timestamp'])
    timestamp = Timestamp('2014-09-07T19:55:00Z')
    cache = {
        revision.metadata: FakeRevisionMetadata(timestamp)
    }
    eq_(solve(day_of_week, cache=cache), 6)


def test_hour_of_day():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata", ['timestamp'])
    timestamp = Timestamp('2014-09-07T19:55:00Z')
    cache = {
        revision.metadata: FakeRevisionMetadata(timestamp)
    }
    eq_(solve(hour_of_day, cache=cache), 19)


# ############################## Comment ######################################
def test_has_custom_comment():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata", ['comment'])

    cache = {
        revision.metadata: FakeRevisionMetadata("I did stuff!")
    }
    assert solve(has_custom_comment, cache=cache)

    cache = {
        revision.metadata: FakeRevisionMetadata(None)
    }
    assert not solve(has_custom_comment, cache=cache)

    cache = {
        revision.metadata: FakeRevisionMetadata("/* Foobar */ I did stuff!")
    }
    assert solve(has_custom_comment, cache=cache)

    cache = {
        revision.metadata: FakeRevisionMetadata("")
    }
    assert not solve(has_custom_comment, cache=cache)

    cache = {
        revision.metadata: FakeRevisionMetadata("/* Foobar */")
    }
    assert not solve(has_custom_comment, cache=cache)


def test_has_section_comment():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata", ['comment'])

    cache = {
        revision.metadata: FakeRevisionMetadata("I did stuff!")
    }
    assert not solve(has_section_comment, cache=cache)

    cache = {
        revision.metadata: FakeRevisionMetadata(None)
    }
    assert not solve(has_section_comment, cache=cache)

    cache = {
        revision.metadata: FakeRevisionMetadata("/* Foobar */ I did stuff!")
    }
    assert solve(has_section_comment, cache=cache)

    cache = {
        revision.metadata: FakeRevisionMetadata("/* Foobar */")
    }
    assert solve(has_section_comment, cache=cache)


# ################################ Bytes ######################################
def test_bytes():
    FakeRevisionMetadata = namedtuple("FakeRevisionMetadata", ["bytes"])
    cache = {
        revision.metadata: FakeRevisionMetadata(45678)
    }
    eq_(solve(bytes, cache=cache), 45678)


# ############################## Characters ###################################
def test_chars():
    cache = {
        revision.text: "Twelve chars"
    }
    eq_(solve(chars, cache=cache), 12)


def test_markup_chars():
    cache = {
        revision.text: "Twelve {{chars}}"
    }
    eq_(solve(markup_chars, cache=cache), 4)


def test_numeric_chars():
    cache = {
        revision.text: "Twelve hats pants 95 bananas!"
    }
    eq_(solve(numeric_chars, cache=cache), 2)


def test_symbolic_chars():
    cache = {
        revision.text: "Twelve hats?  Pants, #95 bananas!"
    }
    eq_(solve(symbolic_chars, cache=cache), 4)


def test_uppercase_chars():
    cache = {
        revision.text: "Twelve hats?  Pants, #95 bananas!"
    }
    eq_(solve(uppercase_chars, cache=cache), 2)


# ############################ Parsed text ####################################
def test_level_1_headings():
    FakeHeading = namedtuple("FakeHeading", ['level'])
    cache = {
        revision.headings: [FakeHeading(2), FakeHeading(3), FakeHeading(4),
                            FakeHeading(2)]
    }
    eq_(solve(level_1_headings, cache=cache), 0)


def test_level_2_headings():
    FakeHeading = namedtuple("FakeHeading", ['level'])
    cache = {
        revision.headings: [FakeHeading(2), FakeHeading(3), FakeHeading(4),
                            FakeHeading(2)]
    }
    eq_(solve(level_2_headings, cache=cache), 2)


def test_level_3_headings():
    FakeHeading = namedtuple("FakeHeading", ['level'])
    cache = {
        revision.headings: [FakeHeading(2), FakeHeading(3), FakeHeading(4),
                            FakeHeading(2)]
    }
    eq_(solve(level_3_headings, cache=cache), 1)


def test_level_4_headings():
    FakeHeading = namedtuple("FakeHeading", ['level'])
    cache = {
        revision.headings: [FakeHeading(2), FakeHeading(3), FakeHeading(4),
                            FakeHeading(2)]
    }
    eq_(solve(level_4_headings, cache=cache), 1)


def test_level_5_headings():
    FakeHeading = namedtuple("FakeHeading", ['level'])
    cache = {
        revision.headings: [FakeHeading(2), FakeHeading(3), FakeHeading(4),
                            FakeHeading(2)]
    }
    eq_(solve(level_5_headings, cache=cache), 0)


def test_level_6_headings():
    FakeHeading = namedtuple("FakeHeading", ['level'])
    cache = {
        revision.headings: [FakeHeading(2), FakeHeading(3), FakeHeading(4),
                            FakeHeading(2)]
    }
    eq_(solve(level_6_headings, cache=cache), 0)


def test_content_chars():
    cache = {
        revision.content: "Thisistwelve"  # 12 characters of content
    }
    eq_(solve(content_chars, cache=cache), 12)


def test_category_links():
    FakeLink = namedtuple("FakeLink", "title")
    cache = {
        revision.internal_links: [FakeLink("Foobar"),
                                  FakeLink("File:Hat.jpg"),
                                  FakeLink("file:Bum.gif"),
                                  FakeLink("Category:Hats")]
    }
    eq_(solve(category_links, cache=cache), 1)


def test_image_links():
    FakeLink = namedtuple("FakeLink", "title")
    cache = {
        revision.internal_links: [FakeLink("Foobar"),
                                  FakeLink("File:Hat.jpg"),
                                  FakeLink("file:Bum.gif"),
                                  FakeLink("Category:Hats")]
    }
    eq_(solve(image_links, cache=cache), 2)


def test_internal_links():
    FakeLink = namedtuple("FakeLink", "title")
    cache = {
        revision.internal_links: [FakeLink("Foobar"),
                                  FakeLink("File:Hat.jpg"),
                                  FakeLink("file:Bum.gif"),
                                  FakeLink("Category:Hats")]
    }
    eq_(solve(internal_links, cache=cache), 4)


def test_ref_tags():
    FakeTag = namedtuple("FakeTag", ['tag'])
    cache = {
        revision.tags: [FakeTag('derp'),
                        FakeTag('ref'),
                        FakeTag('ref'),
                        FakeTag('herp')]
    }
    eq_(solve(ref_tags, cache=cache), 2)


def test_templates():
    FakeTemplate = namedtuple("FakeTemplate", ['name'])
    cache = {
        revision.templates: [FakeTemplate("Hat"),
                             FakeTemplate("Cite"),
                             FakeTemplate("Cite waffle"),
                             FakeTemplate("Research project/Infobox"),
                             FakeTemplate("Infobox"),
                             FakeTemplate("DerpInfobox"),
                             FakeTemplate("Anarchism/Sidebar")]
    }
    eq_(solve(templates, cache=cache), 7)


def test_cite_templates():
    FakeTemplate = namedtuple("FakeTemplate", ['name'])
    cache = {
        revision.templates: [FakeTemplate("Hat"),
                             FakeTemplate("Cite"),
                             FakeTemplate("Cite waffle"),
                             FakeTemplate("Research project/Infobox"),
                             FakeTemplate("Infobox"),
                             FakeTemplate("DerpInfobox"),
                             FakeTemplate("Anarchism/Sidebar")]
    }
    eq_(solve(cite_templates, cache=cache), 2)


def test_infobox_templates():
    FakeTemplate = namedtuple("FakeTemplate", ['name'])
    cache = {
        revision.templates: [FakeTemplate("Hat"),
                             FakeTemplate("Cite"),
                             FakeTemplate("Cite waffle"),
                             FakeTemplate("Research project/Infobox"),
                             FakeTemplate("Infobox"),
                             FakeTemplate("DerpInfobox"),
                             FakeTemplate("Anarchism/Sidebar")]
    }
    eq_(solve(infobox_templates, cache=cache), 4)
