# RepoFix Agent

这是我学习 AI Agent 过程中做的一个小项目。

项目的主要功能是：让 AI Agent 根据用户提供的 Bug 描述，自己去查看 Python 项目中的代码，找到可能有问题的位置，修改代码，然后运行测试来判断修改是否成功。

整个流程大概是：

```text
用户输入 Bug
    ↓
Agent 查看项目文件
    ↓
搜索相关代码
    ↓
读取代码
    ↓
修改代码
    ↓
运行 pytest
    ↓
根据测试结果判断是否修复成功
```

这个项目主要是为了学习 Agent 中比较核心的几个概念，比如 Tool Calling、Agent Loop，以及如何让大模型和本地代码仓库进行交互。

---

## 项目功能

目前实现的功能比较简单：

* 查看项目中的文件
* 根据关键词搜索代码
* 读取指定代码文件
* 修改指定代码
* 自动运行 pytest
* 根据测试结果继续判断
* 在终端显示 Agent 调用了哪些工具
* 可以指定需要处理的本地 Python 项目

目前项目主要用于学习和 Demo，并不是一个完整的代码修复工具。

---

## 项目结构

```text
repo-fix-agent/
│
├── main.py
├── reset_demo.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── repofix/
│   ├── __init__.py
│   ├── agent.py
│   ├── context.py
│   ├── hooks.py
│   │
│   └── tools/
│       ├── __init__.py
│       ├── filesystem.py
│       ├── search.py
│       ├── editor.py
│       └── test_runner.py
│
└── demo_repo/
    ├── calculator.py
    └── test_calculator.py
```

其中几个主要文件：

| 文件               | 作用               |
| ---------------- | ---------------- |
| `main.py`        | 项目的启动入口          |
| `agent.py`       | 创建 RepoFix Agent |
| `context.py`     | 保存当前需要处理的项目路径    |
| `hooks.py`       | 在终端显示工具调用过程      |
| `filesystem.py`  | 查看和读取文件          |
| `search.py`      | 搜索代码             |
| `editor.py`      | 修改代码             |
| `test_runner.py` | 运行 pytest        |

---

## Agent 可以使用的工具

目前我给 Agent 提供了 5 个工具。

### 1. list_files

查看当前项目有哪些文件。

例如：

```text
calculator.py
test_calculator.py
```

---

### 2. search_code

根据关键词搜索代码。

例如搜索：

```text
divide
```

可能得到：

```text
calculator.py:5: def divide(a, b):
test_calculator.py:9: assert divide(10, 2) == 5
```

这样 Agent 就可以知道应该去查看哪个文件。

---

### 3. read_file

读取代码文件。

例如：

```text
read_file("calculator.py")
```

可能得到：

```text
1 | def add(a, b):
2 |     return a + b
3 |
4 |
5 | def divide(a, b):
6 |     return a * b
```

---

### 4. replace_in_file

修改代码中的某一部分。

例如把：

```python
return a * b
```

修改成：

```python
return a / b
```

为了避免 Agent 一次性把整个文件改乱，目前项目使用的是比较简单的精确文本替换方式。

---

### 5. run_tests

运行当前 Python 项目的测试：

```bash
python -m pytest -q
```

测试结果会重新返回给 Agent。

如果测试失败，Agent 可以继续根据错误信息分析问题。

---

## 安装

先克隆项目：

```bash
git clone <你的仓库地址>
cd repo-fix-agent
```

创建虚拟环境：

Windows：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux：

```bash
python -m venv .venv
source .venv/bin/activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

---

## 配置 API Key

在项目根目录创建：

```text
.env
```

内容：

```env
OPENAI_API_KEY=your_api_key_here
```

项目中已经提供：

```text
.env.example
```

`.env` 已经加入 `.gitignore`，不要把自己的 API Key 上传到 GitHub。

---

## 运行 Demo

项目中准备了一个很简单的测试项目：

```text
demo_repo/
```

里面的 `calculator.py` 有一个故意写错的函数：

```python
def divide(a, b):
    return a * b
```

正确逻辑应该是除法。

### 第一步：恢复 Bug

运行：

```bash
python reset_demo.py
```

### 第二步：查看当前测试结果

```bash
python -m pytest demo_repo -q
```

这时候应该可以看到：

```text
1 failed, 1 passed
```

### 第三步：启动 Agent

```bash
python main.py --repo ./demo_repo
```

然后输入：

```text
divide 函数的结果不正确，请找到问题并修复。
```

Agent 会自己尝试：

```text
查看文件
 ↓
搜索 divide
 ↓
读取 calculator.py
 ↓
修改错误代码
 ↓
运行 pytest
```

如果修复成功，最后测试应该变成：

```text
2 passed
```

---

## 一个简单的运行流程

例如：

```text
[Agent] RepoFix started

→ Tool: list_files
✓ Tool: list_files

→ Tool: search_code
✓ Tool: search_code

→ Tool: read_file
✓ Tool: read_file

→ Tool: replace_in_file
✓ Tool: replace_in_file

→ Tool: run_tests
✓ Tool: run_tests
```

整个过程中，不是我提前规定 Agent 必须按照固定顺序调用这些工具，而是模型根据当前拿到的信息决定下一步需要使用什么工具。

---

## 我对 Agent 的理解

做完这个项目之后，我目前对 Agent 的理解是：

普通的大模型调用更像：

```text
用户问题
 ↓
LLM
 ↓
回答
```

而 Agent 更像：

```text
用户问题
 ↓
LLM
 ↓
决定调用工具
 ↓
工具执行
 ↓
得到结果
 ↓
LLM继续判断
 ↓
再次调用工具
 ↓
...
 ↓
最终回答
```

所以这个项目里面最重要的部分其实不是“自动修改代码”，而是这个循环：

```text
思考
 ↓
调用工具
 ↓
获取结果
 ↓
继续判断
```

---

## 为什么要运行测试

如果只是让大模型修改代码，它可能会直接告诉我们：

```text
已经修复完成
```

但实际上代码可能还是有问题。

所以在这个项目中，Agent 修改代码以后必须运行：

```text
pytest
```

通过真实的测试结果来判断修改有没有成功。

整个过程可以简单理解为：

```text
修改代码
 ↓
运行测试
 ↓
失败
 ↓
继续修改
 ↓
再次测试
```

这也是这个项目中我觉得比较重要的一部分。

---

## 一些简单的安全限制

因为 Agent 可以修改本地文件，所以我做了一些比较基础的限制。

### 只能操作指定项目

Agent 只能访问通过：

```bash
--repo
```

指定的项目目录。

例如：

```bash
python main.py --repo ./demo_repo
```

那么工具只能操作 `demo_repo` 中的文件。

### 不提供任意 Shell 命令

项目没有给 Agent 提供：

```text
execute_command(...)
```

这种工具。

Agent 只能调用固定的：

```text
run_tests()
```

这样可以避免模型执行一些不需要的系统命令。

---

## 目前的不足

这个项目现在还是一个比较简单的学习项目，还有很多可以继续改进的地方：

* 目前主要支持 Python 项目
* 代码搜索只是普通关键词搜索
* 修改代码使用的是字符串替换
* 默认只支持 pytest
* 对比较大的代码仓库效果可能不好
* 还没有 Git Diff
* 还没有自动创建 Commit
* 还没有连接 GitHub Issue
* 没有 Docker 沙箱

暂时没有继续增加这些功能，主要是希望先把 Agent 最基本的工作流程理解清楚。

---

## 后续可以继续做的内容

如果后面有时间，我可能会继续尝试：

* 增加 Git Diff
* 支持自定义测试命令
* 使用 AST 分析 Python 代码
* 改进代码搜索
* 自动生成 Git Commit
* 接入 GitHub Issue
* 增加简单的 Agent Evaluation

---

## 项目总结

这个项目比较小，主要是我用来学习 Agent 核心流程的实践项目。

目前我认为一个简单的 Agent 可以理解成：

```text
LLM
+
Tools
+
可以操作的环境
+
工具执行结果
```

在 RepoFix 中分别对应：

```text
LLM
+
代码搜索/读取/修改工具
+
本地 Python 项目
+
pytest 测试结果
```

通过这个项目，我主要实践了 Tool Calling、Agent Loop、本地文件操作以及利用测试结果反馈给 Agent 的基本流程。
