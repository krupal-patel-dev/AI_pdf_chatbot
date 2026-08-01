from typing import Any, List, Tuple

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


def ask_question(
    vector_store: Any,
    question: str,
    top_k: int = 4,
) -> Tuple[str, List[Document]]:
    """
    Retrieve relevant PDF chunks from FAISS
    and generate an answer using Gemini.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    # 1. Retrieve relevant PDF chunks
    retrieved_documents = vector_store.similarity_search(
        question,
        k=top_k,
    )

    if not retrieved_documents:
        return (
            "I could not find relevant information in the uploaded PDF.",
            [],
        )

    # 2. Build context from retrieved chunks
    context_parts = []

    for document in retrieved_documents:
        source = document.metadata.get(
            "source",
            "Unknown file",
        )

        page = document.metadata.get(
            "page",
            "Unknown page",
        )

        chunk_id = document.metadata.get(
            "chunk_id",
            "Unknown chunk",
        )

        context_parts.append(
            f"""
Source: {source}
Page: {page}
Chunk: {chunk_id}

Content:
{document.page_content}
"""
        )

    context = "\n\n".join(context_parts)

    # 3. Create prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an AI PDF question-answering assistant.

Rules:
1. Answer only from the provided PDF context.
2. Do not use outside knowledge.
3. If the answer is not available, say:
   "I could not find this information in the uploaded PDF."
4. Keep the answer clear and concise.
5. Do not invent facts, page numbers, or sources.
""",
            ),
            (
                "human",
                """
PDF context:
{context}

User question:
{question}
""",
            ),
        ]
    )

    # 4. Create Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0,
        max_retries=2,
    )

    # 5. Format and send prompt
    messages = prompt.format_messages(
        context=context,
        question=question,
    )
    response = llm.invoke(messages)

    if isinstance(response.content, str):
        answer = response.content
    elif isinstance(response.content, list):
        answer = ""

        for item in response.content:
            if isinstance(item, dict) and item.get("type") == "text":
                answer += item.get("text", "")
    else:
        answer = str(response.content)

    return answer, retrieved_documents

    # 6. Extract answer safely
    if isinstance(response.content, str):
        answer = response.content
    else:
        answer = str(response.content)

    return answer, retrieved_documents