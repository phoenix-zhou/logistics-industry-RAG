# 📦 Logistics RAG System (Logistics Industry Knowledge Base Q&A)

本项目是一个基于 **RAG (Retrieval-Augmented Generation，检索增强生成)** 技术的本地知识库问答系统。

虽然本项目以 **“物流行业”** 为例进行构建和测试，但系统具有高度的通用性。使用者可以自由切换其他行业类型的知识文档（如金融、医疗、法律等），快速实现私有化的本地知识库问答效果。

## ✨ 主要功能

- **🔍 基于本地知识库的问答**：系统能够根据用户的自然语言提问，在本地向量数据库中进行语义搜索，精准匹配相关文档片段，并返回基于事实的答案。
- **🤖 多模型支持**：
    - **Embedding 模型**：负责将文本转化为向量，支持替换不同的向量化模型以优化检索效果。
    - **LLM (大语言模型)**：负责根据上下文生成最终回答，支持接入 ChatGLM, Qwen, Llama 等多种开源模型。
- **🔒 离线私有化部署**：所有数据处理、向量检索及模型推理均在本地完成，无需联网，确保企业核心数据的安全性和隐私性。
- **⚙️ 灵活扩展**：基于 LangChain 框架开发，易于扩展新的文档加载器或向量存储方案。

## 🛠️ 技术栈

- **编程语言**: Python (3.8 - 3.11)
- **核心框架**: LangChain
- **向量数据库**: FAISS (Facebook AI Similarity Search)
- **模型管理**: Ollama (用于本地运行和管理 LLM)
- **依赖库**: faiss-cpu, langchain, ollama

## ⚙️ 环境配置与安装

### 1. 前置要求
确保你的机器上安装了 Python，推荐版本为 **Python 3.8 - 3.11**。

### 2. 安装依赖
克隆本项目后，进入项目目录，使用 pip 安装所需的第三方库：
pip install faiss-cpu
pip install langchain
pip install ollama
###  3. 模型准备
本项目采用本地离线运行模式，推荐使用 Ollama 来管理和运行大模型。
下载并安装 Ollama。
拉取你需要的模型（例如 Qwen 或 ChatGLM）：
ollama pull qwen:7b  # 或者 ollama pull chatglm3
🚀 快速开始
#### 1. 准备知识库数据
将你的行业知识文档（支持 .txt, .pdf 等格式）放入项目根目录。
示例数据：物流信息.pdf
#### 2. 构建索引与问答
运行主程序脚本（假设主入口为 local_qa.py 或 new_demo.py，请根据实际文件名调整）：
python local_qa.py
#### 3. Web 界面交互 (可选)
如果项目包含 Web UI 脚本（如 web_qa.py），可以启动网页版问答界面：
python web_qa.py
## 🏗️ 项目原理
本系统遵循标准的 RAG 流程，主要分为三个阶段：Retrieve (检索), Augment (增强), Generate (生成)。
详细处理流程：
-- 加载文件 (Load): 读取本地文档（如 PDF, TXT）。
-- 文本分割 (Split): 将长文档切分为较小的文本块 (Chunks)，以便模型处理。
-- 向量化 (Embedding): 使用 Embedding 模型将文本块转化为向量。
-- 存储 (Store): 将向量存入本地向量数据库 (FAISS Index)。
-- 检索 (Retrieve):
        用户输入问题 (Query)。
        将问题向量化。
        在 FAISS 中计算相似度，召回 Top-K 个最相关的文本块。
--生成 (Generate):
        将“用户问题”与“召回的文本块”组装成 Prompt。
        提交给本地 LLM (如 Qwen/ChatGLM)。
        LLM 输出最终答案。
📂 项目结构
```
/
├── faiss_index/          # 生成的向量索引文件夹
├── local_db.py           # 数据库构建与索引逻辑
├── local_qa.py           # 命令行问答主程序
├── new_demo.py           # 演示脚本
├── web_qa.py             # Web 界面启动脚本
├── 物流信息.pdf          # 示例知识库文件
└── README.md             # 项目说明文档
```
## 📝 注意事项
显存要求: 运行本地大模型（如 7B 参数量的模型）通常需要至少 8GB-16GB 的系统内存或显存。
中文支持: 建议在 Ollama 中选择对中文支持较好的模型（如 qwen, chatglm3, yi 等）。
数据安全: 所有数据均存储在本地 faiss_index 目录中，不会上传至云端

##### 对应详细步骤以及解析见博客: https://blog.csdn.net/zhoupenghui168/article/details/162247139
```
