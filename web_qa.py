# 从自定义模块 local_qa 中导入所有必要的组件（如大模型实例、向量数据库 db 等）
from local_qa import *
# 从 LangChain 导入 ConversationalRetrievalChain，该链专门用于处理带有历史上下文的检索问答
# ConversationalRetrievalChain作用：自动保存历史对话信息
from langchain.chains import ConversationalRetrievalChain
# 导入 Streamlit 库，用于快速构建 Web 交互界面
import streamlit as st

# 设置标题
st.set_page_config(page_title="物流行业信息咨询系统")
st.title("物流行业信息咨询RAG系统")

# 初始化全局变量, 用于存储对话历史
# 注意：在 Streamlit 中，每次页面交互都会重新运行整个脚本，普通全局变量无法跨次交互保留状态
chat_history = []


# 定义检索链函数
def new_retrival():
    """
    创建基于 ConversationalRetrievalChain 的问答链
    该链会自动处理：检索相关文档 -> 将文档和历史对话作为上下文 -> 传给大模型生成答案
    """
    chain = ConversationalRetrievalChain.from_llm(
        llm=Ollama(model="qwen2.5:7b"),  # 使用本地大模型
        retriever=db.as_retriever()  # 基于本地数据库的检索器
    )
    return chain


# 主逻辑
def main():
    """
    Streamlit 主页面的交互逻辑, 负责界面渲染和状态管理
    """
    # print(f'st.session_state-->{st.session_state}')
    # 初始化会话状态
    # 初始化 Streamlit 的会话状态（Session State）
    # session_state 是跨页面刷新/交互保留数据的唯一正确方式
    if "messages" not in st.session_state:
        st.session_state.messages = []  # 用于保存聊天记录, 用于在页面上渲染聊天气泡
    # print(f'st.session_state-->{st.session_state}')
    # 展示历史聊天记录, 实现界面的消息回显
    for message in st.session_state.messages:
        # print(f'message["role"]-->{message["role"]}')
        # 根据消息角色（user 或 assistant）创建对应的聊天气泡
        with st.chat_message(message["role"]):
            st.markdown(message["content"])  # 将消息内容以 Markdown 格式渲染显示

    # 接受用户输入
    # prompt = st.chat_input("请输入你的问题:")
    if prompt := st.chat_input("请输入你的问题:"):
        # 保存用户消息到会话状态
        print(f'prompt--》{prompt}')
        # 将用户的输入追加到会话状态的消息列表中
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 显示用户输入: 立即在界面上显示用户的输入内容
        with st.chat_message("user"):
            st.markdown(prompt)

        # 调用模型获取回答: 在界面上创建助手的回复气泡
        with st.chat_message("assistant"):
            # 创建一个空的占位符，通常用于后续实现流式输出（打字机效果）
            message_placeholder = st.empty()
            full_response = ""

            # 调用检索链获取答案: 每次提问时重新创建检索链
            chain = new_retrival()
            # 调用检索链，传入当前问题和对话历史，获取包含答案的字典结果
            result = chain.invoke({"question": prompt, "chat_history": chat_history})
            print(f'result--->{result}')
            # 将当前的问答对追加到全局的 chat_history 列表中，以维持多轮对话记忆
            chat_history.append((prompt, result["answer"]))  # 更新聊天历史
            # 提取大模型生成的最终答案
            assistant_response = result["answer"]
            # 将答案渲染到占位符中
            message_placeholder.markdown(assistant_response)

            # 保存回答到会话状态
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})


# 运行主逻辑
if __name__ == "__main__":
    main()
