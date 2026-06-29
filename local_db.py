from langchain_community.document_loaders import PyMuPDFLoader # 用于加载和读取本地的 PDF 文件
from langchain.text_splitter import RecursiveCharacterTextSplitter # 用于将长文本按规则递归切分成较小的文本块（chunks）
from langchain_community.embeddings import OllamaEmbeddings # 用于调用本地 Ollama 服务中的嵌入模型，将文本转换为向量
from langchain_community.vectorstores import FAISS  # Meta 开源的本地向量数据库，用于存储向量并进行相似度检索


def get_vector():
    # 第一步：加载文档
    loader = PyMuPDFLoader("物流信息.pdf")
    # 将文本转成 Document 对象
    # 调用 load() 方法将 PDF 内容转化为 LangChain 的 Document 对象列表（通常一页对应一个 Document）
    data = loader.load()
    print(f'data-->{data}')
    print(f'len(data):{len(data)}')

    # # 第二步：切分文本
    # 初始化文本分割器 RecursiveCharacterTextSplitter，设置了两个关键参数：
    #   chunk_size=50：每个文本块的最大长度为 50 个字符。
    #   chunk_overlap=20：相邻文本块之间有 20 个字符的重叠，以保证上下文语义的连贯性
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=20)
    # 切割加载的 document
    # 调用 split_documents(data) 对加载的文档进行切分，并打印切分后的文本块数量和具体内容
    split_docs = text_splitter.split_documents(data)
    print("split_docs size:", len(split_docs))
    print(split_docs)
    #
    # # 第三步：初始化 hugginFace 的 embeddings 对象
    # 实例化 OllamaEmbeddings，指定使用 "qwen2.5:7b" 这个嵌入模型。该模型负责将文本转化为计算机可理解的高维向量表示
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    #
    #
    # # 第四步：将 document通过embeddings对象计算得到向量信息并永久存入FAISS向量数据库，并构建 FAISS 向量索引,用于后续匹配查询
    db = FAISS.from_documents(split_docs, embeddings)
    db.save_local("./faiss/wuliu")

if __name__ == '__main__':
    result = get_vector()
