from sklearn import svm


def LinearSVC(Model):
    
    def __init__(self, extractors, *, classifier=None, **kwargs):
        
        self.extractors = list(extractors)
        
        if classifier is not None:
            self.classifier = svm.SVC(**kwargs)
        else:
            self.classifier = classifier
        
        
    def train(self, feature_sets, classes):
        features = [extractor.validate(value)
                    for feature_set in feature_sets
                    for extractor, value in zip(self.extractors, feature_set)]
                
        
        self.classifier.fit(feature_sets, classes)
    
    def test(self, feature_sets, classes):
        
        
        self.classifier.score(feature_sets, classes)
    
    def predict(self, feature_sets, proba=False):
        if not proba:
            self.classifier.predict_proba(feature_sets)
        else:
            self.classifier.predict(feature_sets)
