import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def create_vector_store(chunks):
    """
    Convert document chunks into embeddings
    and store them inside a FAISS vector database.
    """

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    return vector_store


def save_vector_store(vector_store, path="faiss_indexes/index"):
    """
    Save FAISS index to disk.
    """

    vector_store.save_local(path)


def load_vector_store(path="faiss_indexes/index"):
    """
    Load existing FAISS index.
    """

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vector_store