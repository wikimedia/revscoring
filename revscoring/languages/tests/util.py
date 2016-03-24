from nose.tools import eq_


def compare_extraction(extractor, examples, counter_examples,
                       lwrap="", rwrap=""):

    for example in examples:
        wrapped = lwrap + example + rwrap
        eq_(extractor.process(wrapped), [example])
        eq_(extractor.process("Sentence " + wrapped + " sandwich."), [example])
        eq_(extractor.process("Sentence end " + wrapped + "."), [example])
        eq_(extractor.process(wrapped + " start of sentence."), [example])

    for example in counter_examples:
        wrapped = lwrap + example + rwrap
        eq_(extractor.process(wrapped), [])
        eq_(extractor.process("Sentence " + wrapped + " sandwich."), [])
        eq_(extractor.process("Sentence end " + wrapped + "."), [])
        eq_(extractor.process(wrapped + " start of sentence."), [])
