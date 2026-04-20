import os
from langchain_community.document_loaders import PyPDFLoader
import tempfile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()


def get_pdf_text(pdf_docs):
    documents = []
    for pdf in pdf_docs:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf.read())
            tmp_path = tmp_file.name
        # Load using PyPDFLoader (this keeps metadata like page number)
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        documents.extend(docs)

    if not documents:
        raise ValueError("No readable text found in PDF")
    return documents

def get_text_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return text_splitter.split_documents(documents)


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_documents(documents=text_chunks, embedding=embeddings)


def get_conversation_chain(vectorstore):
    if not os.getenv("OPENROUTER_API_KEY"):
        raise ValueError("OPENROUTER_API_KEY not found in .env")
    llm = ChatOpenAI(
        model="meta-llama/llama-3-8b-instruct",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key='answer'   # ⭐ THIS FIXES YOUR ERROR
    )

    template = """You are a helpful AI assistant. Answer the question based only on the provided context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        ),
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt}
    )