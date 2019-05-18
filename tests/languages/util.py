from revscoring.datasources import revision_oriented as ro
from revscoring.dependencies import solve


def simple_eq(a, b):
    return a == b


def compare_extraction(extractor, examples, counter_examples,
                       lwrap="", rwrap="", eq=simple_eq):
    def process(text):
        return solve(extractor, cache={ro.revision.text: text})

    for example in examples:
        wrapped = lwrap + example + rwrap
        assert eq(process(wrapped), [example]), \
              " ".join([repr(wrapped), str(process(wrapped)), str([example])])
        assert eq(process(
            "Sentence " +
            wrapped +
            " sandwich."), [example])
        assert eq(process("Sentence end " + wrapped + "."), [example])
        assert eq(process(wrapped + " start of sentence."), [example])

    for example in counter_examples:
        wrapped = lwrap + example + rwrap
        assert process(wrapped) == [], process(wrapped)
        assert process("Sentence " + wrapped + " sandwich.") == []
        assert process("Sentence end " + wrapped + ".") == []
        assert process(wrapped + " start of sentence.") == []
