# coding:utf-8
# 导入必备的工具包
import time
from local_db import * # 从自定义模块 local_db 导入了 FAISS
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama

# 加载FAISS向量库
# 初始化了 OllamaEmbeddings 嵌入模型（注意：这里指定了 mxbai-embed-large 作为嵌入模型,
# 通常嵌入模型应该是专门的 embedding 模型如 mxbai-embed-large
embeddings = OllamaEmbeddings(model="mxbai-embed-large", temperature=0)
# 使用 FAISS.load_local 加载了之前保存的向量库，
# 并开启了 allow_dangerous_deserialization=True（这是新版 LangChain 加载本地 FAISS 必须的参数
db = FAISS.load_local("faiss/wuliu", embeddings, allow_dangerous_deserialization=True)
# db = FAISS.load_local("faiss/wuliu", embeddings)

start_time = time.time()


def get_related_content(related_docs):
    """
    文档检索与内容提取
    :param related_docs: 接收检索到的文档列表 related_doc
    :return:
    """
    # print(f'related_docs--》{related_docs}')
    related_content = []
    for doc in related_docs: # 遍历文档，提取 page_content 并用 \n 替换掉 \n\n（为了压缩 Prompt 长度）
        # print(f'doc.page_content--》{doc.page_content}')
        related_content.append(doc.page_content.replace("\n\n", "\n"))
    # print(f'related_content列表状态--》{related_content}')
    # 将所有相关文档的内容拼接成一个完整的字符串返回
    return "\n".join(related_content)


def define_prompt():
    # 硬编码了一个测试问题：'我的快递出发地是哪？预计几天的时间到达？'
    question = '我的快递出发地是哪？预计几天的时间到达？'
    # 调用 db.similarity_search(question, k=2) 从向量库中检索出与问题最相似的 2 个文本块
    docs = db.similarity_search(question, k=2)
    #
    related_content = get_related_content(docs)
    # print('*' * 80)
    # print(f'related_content字符串状态-->{related_content}')
    # print('*'*80)
    # 定义了 Prompt 模板，要求模型“基于已知信息回答，不允许编造”
    PROMPT_TEMPLATE = """
        基于以下已知信息，简洁和专业的来回答用户的问题。不允许在答案中添加编造成分。
        已知内容:
        {context}
        问题:
        {question}"""

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE, )

    my_pmt = prompt.format(context=related_content, question=question)

    return my_pmt


def qa():
    model = Ollama(model="qwen2.5:7b")
    # print(f'model-->{model}')
    my_pmt = define_prompt()
    print(f'my_pmt--》{my_pmt}')
    result = model.invoke(my_pmt)
    return result


if __name__ == '__main__':
    result = qa()
    print(result)
    end_time = time.time()
    print(end_time - start_time)
