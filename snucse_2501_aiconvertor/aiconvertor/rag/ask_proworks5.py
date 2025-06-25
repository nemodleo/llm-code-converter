from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings


def ask_proworks5(embedding_model_name, llm_model_name, vectorstore_path):
    embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vectorstore = FAISS.load_local(
        vectorstore_path,
        embedding_model,
        allow_dangerous_deserialization=True
    )
    llm = Ollama(model=llm_model_name)
    prompt = PromptTemplate(
        template="""
다음 ProWorks5 문서 내용을 바탕으로 질문에 성실히 답해줘.

문서:
{context}

질문:
{question}
""",
        input_variables=["context", "question"]
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )  

    while True:
        q = input("질문 (엔터로 종료): ").strip()
        if not q:
            break
        result = qa_chain(q)

        print("\n📚 참조한 문서 청크:\n")
        for i, doc in enumerate(result["source_documents"]):
            print(f"[{i+1}] {doc.page_content[:]}...\n")

        print("\n🧠 답변:\n", result["result"])


if __name__ == "__main__":
    embedding_model_name = "microsoft/codebert-base" #"BAAI/bge-base-en-v1.5"
    # embedding_model_name = "nlpai-lab/KURE-v1"
    llm_model_name = "devstral:24b" #"llama3.2:3b"
    vectorstore_path = f"data/db/proworks5_vectorstore_{embedding_model_name.split('/')[-1]}"

    ask_proworks5(embedding_model_name, llm_model_name, vectorstore_path)
