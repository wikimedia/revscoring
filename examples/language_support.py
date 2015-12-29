from revscoring.datasources.revision_oriented import revision
from revscoring.dependencies import solve
from revscoring.languages import english, spanish

features = [english.informals.revision.matches,
             spanish.informals.revision.matches]
values = solve(features, cache={revision.text: "I think it is stupid."})

for feature, value in zip(features, values):
    print("\t{0}: {1}".format(feature, repr(value)))
