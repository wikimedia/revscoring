from ..datasources import user_info
from .feature import Feature


def process(user_info):
    
    return "bot" in user_info.groups

user_is_bot = Feature("user_is_bot", process,
                      returns=bool, depends_on=[user_info])
