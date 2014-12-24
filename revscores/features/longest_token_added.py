from ..datasources import revision_diff
from .feature import Feature


def process(revision_diff):
    
    longest = 0
    
    operations, a, b = revision_diff
    
    for operation in operations:
        if operation.name == "insert":
            
            for token in b[operation.b1:operation.b2]:
                
                longest = max(longest, len(token))
            
        
    
    return longest

longest_token_added = Feature("longest_token_added", process,
                              returns=int, depends_on=[revision_diff])
