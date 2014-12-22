from ..datasources import revision_diff
from .feature import feature_processor


@feature_processor(returns=int, depends_on=[revision_diff])
def longest_token_added(revision_diff):
    
    longest = 0
    
    operations, a, b = revision_diff
    
    for operation in operations:
        if operation.name == "insert":
            
            for token in b[operation.b1:operation.b2]:
                
                longest = max(longest, len(token))
            
        
    
    return longest
