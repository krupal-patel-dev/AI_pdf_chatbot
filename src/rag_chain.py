from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def ask_question(
    vector_store: Any,
    question: str,
    top_k: int = 4,
):
    """
    Retrieve relevant PDF chunks and generate an answer.
    """

    retrieved_documents = vector_store.similarity_search(
        question,
        k=top_k,
    )

    context_parts = []

    for document in retrieved_documents:
        source = document.metadata.get("source", "Unknown file")
        page = document.metadata.get("page", "Unknown page")
        chunk_id = document.metadata.get("chunk_id", "Unknown chunk")

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

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an AI PDF assistant.

Rules:
1. Answer only from the provided PDF context.
2. Do not use outside knowledge.
3. If the answer is missing, say:
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

Question:
{question}
""",
            ),
        ]
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    messages = prompt.format_messages(
        context=context,
        question=question,
    )

    response = llm.invoke(messages)

    return response.content, retrieved_documents