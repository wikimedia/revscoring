from ..datasources import revision_diff
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[revision_diff])
@returns(int)
def longest_token_added(revision_diff):
    
    longest = 0
    
    operations, a, b = revision_diff
    
    for operation in operations:
        if operation.name == "insert":
            
            for token in b[operation.b1:operation.b2]:
                
                longest = max(longest, len(token))
            
        
    
    return longest
