"""
selectors: (Datasource or FeatureVector)+ --> Feature
 - min
 - max

aggregators: Datasource or FeatureVector --> Feature
 - min
 - max
 - any
 - all
 - len
 - sum
 - mean
 - median
 - stddev
 - ...

operators: (Feature or FeatureVector)+ --> Feature or FeatureVector
 - add
 - sub
 - div
 - mul
 - not
 - and
 - or

rescalers: (Feature or FeatureVector)+ --> Feature of FeatureVector
 - log
 - exp
 - abs
"""
