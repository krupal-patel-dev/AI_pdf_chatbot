from typing import List

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


def create_vector_store(
    chunks: List[Document],
) -> FAISS:
    if not chunks:
        raise ValueError("No document chunks were provided.")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
    )

    return FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )


def save_vector_store(
    vector_store: FAISS,
    path: str = "faiss_indexes/index",
) -> None:
    vector_store.save_local(path)


def load_vector_store(
    path: str = "faiss_indexes/index",
) -> FAISS:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
    )

    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True,
    )