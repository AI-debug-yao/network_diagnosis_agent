# 网络故障诊断智能系统

使用 LangChain 框架和通义千问 LLM 构建的智能网络故障诊断系统。

## 功能特点

- 🔗 通义千问 LLM 集成
- 🧠 ReAct 推理模式
- 🔧 多种网络诊断工具
- 🔗 工具间串联调用
- 💬 会话记忆功能
- 🌐 美观的网页界面

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（如果还没有）
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

复制环境变量模板文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的通义千问 API Key：

```
DASHSCOPE_API_KEY=你的_api_key_这里
```

### 3. 运行应用

#### 方式一：网页界面（推荐）

```bash
source .venv/bin/activate
streamlit run app.py
```

然后在浏览器中打开显示的地址（通常是 http://localhost:8501）
！[运行结果]（./network_diagnosis_agent.png）

#### 方式二：命令行界面

```bash
source .venv/bin/activate
python network_diagnosis.py
```

## 可用的网络诊断工具

- `ping` - 测试主机连通性
- `traceroute` - 追踪路由路径
- `nslookup` - 查询 DNS 解析记录
- `check_port` - 检查端口是否开放（格式：host:port）
- `get_local_network_info` - 获取本地网络信息

## 示例问题

- "为什么我访问不了 google.com？
- "帮我检查 github.com 的连通性"
- "检查一下本地 8080 端口是否开放"
