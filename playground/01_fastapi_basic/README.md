# 阶段 1：FastAPI 最小接口

这是阶段 1 的主体实现目录。

当前目标是完成一个最小可运行的 FastAPI 应用，包含：

- `GET /health`
- `POST /items`
- `GET /items/{item_id}`

## 当前实现模式

本次采用：

- `模式 A：用户主写`

也就是：

- Codex 先搭文件骨架
- 用户补主体逻辑
- Codex 再检查、纠偏、解释

## 你现在要做什么

先打开：

- [main.py](/home/tkp666/FlowRAG/playground/01_fastapi_basic/main.py)

把里面的 3 个 `TODO` 补完。

## 运行命令

```bash
conda activate flowrag
cd /home/tkp666/FlowRAG/playground/01_fastapi_basic
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## 完成后要测试的命令

```bash
curl http://127.0.0.1:8000/health
```

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"demo","description":"first item"}'
```

```bash
curl http://127.0.0.1:8000/items/1
```

## 自查重点

完成后你要自己确认：

1. `GET /health` 能返回 JSON
2. `POST /items` 能把新 item 存进内存
3. `GET /items/{item_id}` 能按 id 读回 item
4. `/docs` 能打开
5. 你能指出：
   - 哪个是 `path parameter`
   - 哪个是 `request body`
   - 哪个是 `response body`
   - 为什么当前先用内存 `dict`
