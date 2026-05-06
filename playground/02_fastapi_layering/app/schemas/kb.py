from pydantic import BaseModel


# TODO:
# 你先在这个文件里补 3 个 schema：
# 1. KBCreate
# 2. KBResponse
# 3. KBListItem
#
# 要求：
# - KBCreate：用于 POST /knowledge-bases 的请求体
# - KBResponse：用于单个知识库详情响应
# - KBListItem：用于知识库列表响应
# - 这 3 个类都继承 BaseModel
# - 字段先保持最小，不要提前加 created_at 之类当前阶段不需要的字段

class KBCreate(BaseModel):
    name: str
    description: str | None = None

class KBResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    
    
class KBListItem(BaseModel):
    id: int
    name: str
    description: str | None = None