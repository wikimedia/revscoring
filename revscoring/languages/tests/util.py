

def compare_extraction(extractor, examples, counter_examples,
                       lwrap="", rwrap=""):

    for example in examples:
        wrapped = lwrap + example + rwrap
        print(extractor.process(wrapped))
        assert extractor.process(wrapped) == [example]
        assert extractor.process(
            "Sentence " +
            wrapped +
            " sandwich.") == [example]
        assert extractor.process("Sentence end " + wrapped + ".") == [example]
        assert extractor.process(wrapped + " start of sentence.") == [example]

    for example in counter_examples:
        wrapped = lwrap + example + rwrap
        assert extractor.process(wrapped) == []
        assert extractor.process("Sentence " + wrapped + " sandwich.") == []
        assert extractor.process("Sentence end " + wrapped + ".") == []
        assert extractor.process(wrapped + " start of sentence.") == []
