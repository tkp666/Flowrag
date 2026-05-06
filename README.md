# FlowRAG Codex Starter

这是 FlowRAG 项目驱动学习的初始化模板。

## 使用方式

1. 解压本目录；
2. 将文件夹改名为 `FlowRAG`；
3. 进入目录并初始化 Git：

```bash
cd FlowRAG
git init
```

4. 在该目录下打开 Codex；
5. 将 `prompts/FIRST_CODEX_PROMPT.txt` 的内容完整复制给 Codex；
6. 从 `playground/01_fastapi_basic/` 开始做预备小实验。

## 文件说明

```text
AGENTS.md                  # 给 Codex 的短规则，控制行为和边界
docs/PROJECT_CONTEXT.md    # 用户背景、求职目标、项目定位、学习方式
docs/STAGE_GUIDE.md        # 7 个预备实验的详细阶段要求
docs/LEARNING_LOG.md       # 每阶段学习记录
docs/STAGE_REPORT.md       # 每阶段验收报告
prompts/FIRST_CODEX_PROMPT.txt # 第一次发给 Codex 的提示词
prompts/STAGE_PROMPTS.md       # 后续每阶段启动提示词模板
```

## 当前策略

当前不要直接开发完整 FlowRAG 主项目。

先完成 7 个预备小实验：

1. FastAPI 最小接口；
2. FastAPI 分层结构；
3. MySQL + SQLAlchemy；
4. Redis 基础；
5. Celery 异步任务；
6. Qdrant 最小向量检索；
7. 流式接口。

完成后再进入正式 FlowRAG 主项目。
