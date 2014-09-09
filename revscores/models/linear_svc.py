from sklean import svm


def LinearSVC(Model):
    
    def __init__(self, feature_extractors, *, classifier=None, **kwargs):
        
        self.feature_extractors = list(feature_extractors)
        
        if classifier is not None:
            self.classifier = svm.SVC(**kwargs)
        else:
            self.classifier = classifier
        
        
    def train(self, feature_sets, classes):
        features = [definition.validate(f)
                    for definition, f in zip(self.feature_set, features)]
                
        
        self.classifier.fit(features, classes)
    
    def test(self, feature_sets, classes):
        features = [extractor.validate(value)
                    for feature_set in feature_sets
                    for extractor, value in zip(self.feature_extractors, feature_set)]
                
        
        self.classifier.score(features, classes)
    
    def predict(self, features, proba=False):
        if not proba:
            self.classifier.predict_proba(features)
        else:
            self.classifier.predict(features)
