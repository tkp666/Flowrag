"""
第 2 阶段 · 第 5 小节动手题

本题重点：
- 不再练业务逻辑本身
- 只练“router / schema / service / repository / app 入口”最后应该落到哪个文件

你要做的事情：
1. 阅读下面的 10 个“代码元素”
2. 把它们分别填写到正确的目标文件路径里
3. 补完底部的 3 个文字回答

可选目标文件只能从这 5 个里选：
- app/main.py
- app/api/kb_router.py
- app/schemas/kb.py
- app/services/kb_service.py
- app/repositories/kb_repository.py

自查方式：
1. 完成后运行：
   python section_05_directory_landing.py
2. 如果全部填写正确，你应该看到：
   all placements look good
"""


VALID_TARGETS = {
    "app/main.py",
    "app/api/kb_router.py",
    "app/schemas/kb.py",
    "app/services/kb_service.py",
    "app/repositories/kb_repository.py",
}


ITEMS = {
    "item_1": "app = FastAPI()",
    "item_2": "app.include_router(kb_router)",
    "item_3": "@router.post('/knowledge-bases')",
    "item_4": "def create_kb(payload: KBCreate): return kb_service_create(payload, owner_id=1001)",
    "item_5": "class KBCreate(BaseModel): ...",
    "item_6": "class KBDetailResponse(BaseModel): ...",
    "item_7": "def kb_service_create(payload, owner_id): 重名检查 + 生成 id + 调 repository_insert + 返回 KBResponse",
    "item_8": "def kb_service_detail(kb_id): 查 kb + 查文档数 + 查标题预览 + 组装 KBDetailResponse",
    "item_9": "def kb_repository_insert(record): ...",
    "item_10": "def doc_repository_count_active_by_kb_id(kb_id): ...",
}


# 第 2 阶段 · 第 5 小节动手题：
# 你要把每个 item 填到它最适合落下去的目标文件路径里。
# 只能填写上面 VALID_TARGETS 里的 5 个路径之一。
#
# 例如：
# item_x = "app/services/kb_service.py"
#
# 提示：
# - app/main.py 只负责应用入口和 router 注册
# - api/kb_router.py 放路由函数和 HTTP 入口
# - schemas/kb.py 放各种请求体 / 响应体 schema
# - services/kb_service.py 放业务规则、流程编排、响应组装
# - repositories/kb_repository.py 放底层数据存取能力


item_1 = "app/main.py"
item_2 = "app/main.py"
item_3 = "app/api/kb_router.py"
item_4 = "app/api/kb_router.py"
item_5 = "app/schemas/kb.py"
item_6 = "app/schemas/kb.py"
item_7 = "app/services/kb_service.py"
item_8 = "app/services/kb_service.py"
item_9 = "app/repositories/kb_repository.py"
item_10 = "app/repositories/kb_repository.py"


EXPECTED = {
    "item_1": "app/main.py",
    "item_2": "app/main.py",
    "item_3": "app/api/kb_router.py",
    "item_4": "app/api/kb_router.py",
    "item_5": "app/schemas/kb.py",
    "item_6": "app/schemas/kb.py",
    "item_7": "app/services/kb_service.py",
    "item_8": "app/services/kb_service.py",
    "item_9": "app/repositories/kb_repository.py",
    "item_10": "app/repositories/kb_repository.py",
}


# 文字回答区：
#
# 1. 为什么 app/main.py 在分层后应该尽量变薄？
# 答：在分层后app/main.py应该只做应用入口和 router 注册，其余应该交给别的层做
#
# 2. 为什么 router 已经放进 api/ 目录后，仍然不应该直接写业务逻辑？
# 答：业务逻辑应该交由service来做
#
# 3. 为什么完整目录结构不是“为了好看”，而是“为了让职责真正落位”？
# 答：是为了分层啊，每层都有自己对应的职责， 不能多管也不能啥也不干


def collect_answers() -> dict[str, str]:
    return {
        "item_1": item_1,
        "item_2": item_2,
        "item_3": item_3,
        "item_4": item_4,
        "item_5": item_5,
        "item_6": item_6,
        "item_7": item_7,
        "item_8": item_8,
        "item_9": item_9,
        "item_10": item_10,
    }


def main() -> None:
    answers = collect_answers()

    for key, value in answers.items():
        if value not in VALID_TARGETS:
            raise ValueError(f"{key} 还没填对目标路径：{value!r}")

    for key, expected in EXPECTED.items():
        actual = answers[key]
        if actual != expected:
            raise ValueError(
                f"{key} 放错了。当前是 {actual}，正确应为 {expected}。"
            )

    print("all placements look good")


if __name__ == "__main__":
    main()
