from embedding_loader import EmbeddingLoader
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader

from langchain.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from zhipuai import ZhipuAI
 # 需要下载源码
from zhipuai_llm import ZhipuAILLM

from dotenv import find_dotenv, load_dotenv
import os

# 读取本地/项目的环境变量。

# find_dotenv()寻找并定位.env文件的路径
# load_dotenv()读取该.env文件，并将其中的环境变量加载到当前的运行环境中
# 如果你设置的是全局的环境变量，这行代码则没有任何作用。
_ = load_dotenv(find_dotenv())

# 获取环境变量 API_KEY
api_key = os.environ["ZHIPUAI_API_KEY"] #填写控制台中获取的 APIKey 信息

zhipuai_model = ZhipuAILLM(model = "glm-4", temperature = 0.1, api_key = api_key)  #model="glm-4-0520",

# 定义持久化路径
persist_directory = '/root/learning_assistant/knowledge_data/vector_db/chroma'
# 指定文件夹路径
folder_path = "/root/learning_assistant/knowledge_data"

# 知识库中单段文本长度
CHUNK_SIZE = 500

# 知识库中相邻文本重合长度
OVERLAP_SIZE = 50

def load_md_files(folder_path):
    """
    递归加载指定文件夹及其所有子目录中的所有 Markdown 文件并返回加载后的内容列表。

    参数：
    folder_path (str): 文件夹路径

    返回：
    list: 包含所有 Markdown 文件加载后内容的列表
    """
    md_files = []
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".md"):
                file_path = os.path.join(root, filename)
                loader = UnstructuredMarkdownLoader(file_path)
                md_content = loader.load()
                md_files.extend(md_content)
    return md_files


def vector_db_build(BCembedding):
    # 加载文件夹及其子目录中的所有 Markdown 文件
    md_pages = load_md_files(folder_path)

    # 使用递归字符文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=OVERLAP_SIZE
    )
    split_docs = text_splitter.split_documents(md_pages)

    vectordb = Chroma.from_documents(
        documents=split_docs, 
        embedding=BCembedding,
        persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    )


    return vectordb



def create_qa_chain(BCembedding):
    template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
    案。”。
    {context}
    问题: {question}
    """

    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],
                                    template=template)
    vectordb = Chroma(embedding_function=BCembedding,persist_directory=persist_directory)

    qa_chain = RetrievalQA.from_chain_type(zhipuai_model,
                                        retriever=vectordb.as_retriever(),
                                        return_source_documents=True,
                                        chain_type_kwargs={"prompt":QA_CHAIN_PROMPT})
    
    return qa_chain



def main():
    BCembedding = EmbeddingLoader.get_instance()
   
    if os.path.isdir(persist_directory):
        print(f"The vectordb '{persist_directory}' exists.")
        
    else:
        print(f"The vectordb '{persist_directory}' does not exist.")
        print("Building a new vectordb...")
        vector_db_build(BCembedding)

    qa_chain = create_qa_chain(BCembedding)

    while True:
        question = input("user:")

        result = qa_chain.invoke({"query": question})
        print("bot:" + result["result"])


if __name__ == "__main__":
    main()