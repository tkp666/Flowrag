# 第 2 阶段综合课后动手题：分层结构蓝图

本题不是让你立刻开始阶段 2 的主体实现，而是先把“完整分层结构应该怎么落地”想清楚。

## 作业目标

请你基于这一阶段已经学过的内容，写出一个最小但清晰的 FastAPI 分层蓝图。

你要围绕的业务对象是：

- `knowledge-bases`

你要覆盖的接口是：

- `POST /knowledge-bases`
- `GET /knowledge-bases`
- `GET /knowledge-bases/{kb_id}`
- `DELETE /knowledge-bases/{kb_id}`

---

## 你要完成的内容

### 1. 写出目录蓝图

至少包含下面这些文件：

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

你可以直接用代码块写出来。

### 2. 说明每个关键文件放什么、不放什么

至少说明下面这 5 个文件：

- `app/main.py`
- `app/api/kb_router.py`
- `app/schemas/kb.py`
- `app/services/kb_service.py`
- `app/repositories/kb_repository.py`

每个文件写 2-4 句即可，至少回答：

1. 这个文件主要放什么；
2. 这个文件不该放什么；
3. 为什么这样分。

### 3. 写出调用链说明

请分别说明下面 3 个接口的调用链：

#### `POST /knowledge-bases`

至少写清楚：

- router 收到什么
- service 做什么
- repository 做什么
- 最后返回什么 schema

#### `GET /knowledge-bases/{kb_id}`

至少写清楚：

- router 收到什么
- service 做什么判断
- repository 查什么
- 最后返回什么 schema

#### `DELETE /knowledge-bases/{kb_id}`

至少写清楚：

- router 收到什么
- service 做什么判断
- repository 执行什么操作
- 返回什么结果

### 4. 写出“最容易写错的 5 个点”

请你结合阶段 2 已经学过的内容，总结 5 个最容易犯的错误。

例如你可以从这些方向想：

- router 越权
- service 变空壳
- schema 和 repository 混在一起
- response schema 放错位置
- 目录结构有了但职责没分清

---

## 输出格式建议

你可以按下面这个结构写：

```markdown
# 阶段 2 分层结构蓝图

## 目录蓝图

## 文件职责说明

### app/main.py

### app/api/kb_router.py

### app/schemas/kb.py

### app/services/kb_service.py

### app/repositories/kb_repository.py

## 调用链说明

### POST /knowledge-bases

### GET /knowledge-bases/{kb_id}

### DELETE /knowledge-bases/{kb_id}

## 最容易写错的 5 个点
```

---

## 自查标准

写完后你自己检查这 4 件事：

1. 你有没有把 router / service / repository / schema 的职责说混；
2. 你有没有让 `main.py` 变成新的大杂烩；
3. 你有没有把“调用链”写成只描述文件名，而没写清楚每层到底做什么；
4. 你有没有把“最容易写错的点”写成空话，而没有结合阶段 2 已学内容。

---

## 完成后怎么告诉我

你写完后，直接回我：

```text
阶段2综合作业我写完了
```
