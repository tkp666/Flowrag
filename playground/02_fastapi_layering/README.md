# 阶段 2：FastAPI 分层结构

本实验目标：

- 练习 `router / service / repository / schema` 分层；
- 实现最小知识库接口：
  - `POST /knowledge-bases`
  - `GET /knowledge-bases`
  - `GET /knowledge-bases/{kb_id}`
  - `DELETE /knowledge-bases/{kb_id}`
- repository 继续先用内存存储模拟，不接数据库。

## 目录结构

```text
playground/02_fastapi_layering/
  README.md
  requirements.txt
  app/
    main.py
    api/
      kb_router.py
    schemas/
      kb.py
    services/
      kb_service.py
    repositories/
      kb_repository.py
```

## 运行命令

```bash
conda activate flowrag
cd /home/tkp666/FlowRAG/playground/02_fastapi_layering
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## 测试命令

```bash
curl -X POST http://127.0.0.1:8000/knowledge-bases \
  -H "Content-Type: application/json" \
  -d '{"name":"demo-kb","description":"first kb"}'
```

```bash
curl http://127.0.0.1:8000/knowledge-bases
```

```bash
curl http://127.0.0.1:8000/knowledge-bases/1
```

```bash
curl -X DELETE http://127.0.0.1:8000/knowledge-bases/1
```

```bash
curl http://127.0.0.1:8000/knowledge-bases/999
```

```text
http://127.0.0.1:8000/docs
```

## 当前说明

当前骨架已创建，但核心逻辑会按课堂模式逐步补完，不会一次性全部写满。
