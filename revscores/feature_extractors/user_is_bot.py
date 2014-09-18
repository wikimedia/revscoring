from ..datasources import user_info
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[user_info])
@returns(bool)
def user_is_bot(user_info):
    
    return "bot" in user_info.groups
