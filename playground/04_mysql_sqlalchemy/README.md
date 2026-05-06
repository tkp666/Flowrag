# 阶段 4：MySQL + SQLAlchemy 基础

本目录是 FlowRAG 预备营阶段 4 的主体实现骨架。

当前采用模式 A：用户主写。Codex 已经创建分层结构、SQLAlchemy model、Pydantic schema、router 和运行说明；核心 repository / service 逻辑由用户补全。

## 文件职责

```text
app/db.py            engine、SessionLocal、get_db、init_db
app/models.py        UserModel、KnowledgeBaseModel
app/schemas.py       API 请求/响应 schema
app/repositories.py  SQLAlchemy 数据库读写 TODO
app/services.py      业务规则和 model -> schema 转换 TODO
app/routers.py       FastAPI 路由入口
app/main.py          FastAPI app 和路由注册
```

## 安装依赖

```bash
cd /home/tkp666/FlowRAG/playground/04_mysql_sqlalchemy
/home/tkp666/miniconda3/envs/flowrag/bin/pip install -r requirements.txt
```

## 运行方式

如果本机已经有 MySQL，并且已经创建好数据库：

```bash
export DATABASE_URL="mysql+pymysql://用户名:密码@127.0.0.1:3306/flowrag_stage4"
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn app.main:app --reload
```

如果只是先检查 app 能否启动，可以不设置 `DATABASE_URL`，默认会用当前目录下的 SQLite 文件 `stage4_local.db`。

## 建库示例

```sql
CREATE DATABASE flowrag_stage4 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 自测接口

```bash
curl http://127.0.0.1:8000/health
```

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email":"a@example.com","username":"alice"}'
```

```bash
curl -X POST "http://127.0.0.1:8000/knowledge-bases?current_user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"name":"paper-kb","description":"论文知识库"}'
```

```bash
curl "http://127.0.0.1:8000/knowledge-bases?current_user_id=1&page=1&page_size=10"
```

## 一键检查脚本

主体实现完成后，可以先不启动 MySQL 和 uvicorn，直接运行检查脚本：

```bash
cd /home/tkp666/FlowRAG/playground/04_mysql_sqlalchemy
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage4.py
```

如果全部通过，会输出：

```text
100分：阶段 4 主体实现检查全部通过
```

如果失败，会输出失败的检查项、错误类型、错误信息和 traceback。

更详细的检查可以运行：

```bash
cd /home/tkp666/FlowRAG/playground/04_mysql_sqlalchemy
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage4_detailed.py
```

它会额外检查：

```text
service / repository 的细粒度边界
router 的错误状态码映射
响应体是否暴露内部字段
更新知识库时 id 是否稳定
更新为自己的原名称是否被误判重复
软删除后同名重建的当前策略
```

## 你需要补全

先补：

```text
app/repositories.py
```

再补：

```text
app/services.py
```

验收目标：

```text
能创建 user
能创建 knowledge_base
能分页查询当前用户未删除知识库
能查询详情
能更新知识库
能软删除知识库
软删除后列表不再返回
不能访问、修改、删除别人的知识库
```
