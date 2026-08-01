import streamlit as st
from dotenv import load_dotenv

from src.document_loader import load_pdf
from src.rag_chain import ask_question
from src.text_splitter import split_documents
from src.vector_store import create_vector_store


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

# --------------------------------------------------
# 2. Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="📄",
    layout="wide",
)


# --------------------------------------------------
# 3. Initialize session state
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "pdf_page_count" not in st.session_state:
    st.session_state.pdf_page_count = 0

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "documents" not in st.session_state:
    st.session_state.documents = []

if "chunks" not in st.session_state:
    st.session_state.chunks = []


# --------------------------------------------------
# 4. Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("📁 Document Upload")

    uploaded_file = st.file_uploader(
        "Upload a PDF file",
        type=["pdf"],
        help="Only text-based PDF files are supported.",
    )

    process_button = st.button(
        "Process PDF",
        type="primary",
        use_container_width=True,
    )

    if process_button:
        if uploaded_file is None:
            st.warning("Please upload a PDF first.")

        else:
            try:
                with st.spinner("Processing PDF..."):
                    # Step 1: Read PDF pages
                    documents = load_pdf(uploaded_file)

                    if not documents:
                        raise ValueError(
                            "No readable text was found in the PDF."
                        )

                    # Step 2: Split pages into chunks
                    chunks = split_documents(
                        documents=documents,
                        chunk_size=1000,
                        chunk_overlap=200,
                    )

                    if not chunks:
                        raise ValueError(
                            "No text chunks were created."
                        )

                    # Step 3: Create embeddings and FAISS index
                    vector_store = create_vector_store(chunks)

                    # Step 4: Save results in session state
                    st.session_state.documents = documents
                    st.session_state.chunks = chunks
                    st.session_state.vector_store = vector_store
                    st.session_state.pdf_page_count = len(documents)
                    st.session_state.chunk_count = len(chunks)
                    st.session_state.pdf_processed = True
                    st.session_state.uploaded_file_name = (
                        uploaded_file.name
                    )
                    st.session_state.messages = []

                st.success("PDF processed successfully.")

            except Exception as error:
                st.session_state.pdf_processed = False
                st.session_state.vector_store = None

                st.error(
                    f"Unable to process PDF: {error}"
                )

    st.divider()

    st.subheader("Document Status")

    if st.session_state.pdf_processed:
        st.success("Ready for questions")

        st.write(
            f"**File:** {st.session_state.uploaded_file_name}"
        )

        st.write(
            f"**Pages loaded:** "
            f"{st.session_state.pdf_page_count}"
        )

        st.write(
            f"**Chunks created:** "
            f"{st.session_state.chunk_count}"
        )

    else:
        st.info("No PDF processed yet")

    st.divider()

    clear_button = st.button(
        "Clear Chat",
        use_container_width=True,
    )

    if clear_button:
        st.session_state.messages = []
        st.rerun()

    reset_button = st.button(
        "Reset Document",
        use_container_width=True,
    )

    if reset_button:
        st.session_state.messages = []
        st.session_state.pdf_processed = False
        st.session_state.uploaded_file_name = None
        st.session_state.pdf_page_count = 0
        st.session_state.chunk_count = 0
        st.session_state.vector_store = None
        st.session_state.documents = []
        st.session_state.chunks = []
        st.rerun()


# --------------------------------------------------
# 5. Main page heading
# --------------------------------------------------
st.title("📄 AI PDF Chatbot")

st.write(
    "Upload a PDF document and ask questions about its content."
)

st.caption(
    "Built using Python, Streamlit, LangChain, FAISS, and Gemini."
)



# --------------------------------------------------
# 6. Instructions and document preview
# --------------------------------------------------
if not st.session_state.pdf_processed:
    st.info(
        "Upload a PDF from the sidebar and click "
        "**Process PDF** to begin."
    )

else:
    with st.expander("Preview Extracted PDF Pages"):
        for index, document in enumerate(
            st.session_state.documents[:3],
            start=1,
        ):
            page_number = document.metadata.get(
                "page",
                index,
            )

            st.markdown(f"### Page {page_number}")
            st.write(document.page_content[:1500])
            st.divider()

    with st.expander("Preview Text Chunks"):
        for index, chunk in enumerate(
            st.session_state.chunks[:5],
            start=1,
        ):
            page_number = chunk.metadata.get(
                "page",
                "Unknown",
            )

            chunk_id = chunk.metadata.get(
                "chunk_id",
                index,
            )

            st.markdown(
                f"### Chunk {chunk_id} — Page {page_number}"
            )

            st.write(chunk.page_content)
            st.divider()


# --------------------------------------------------
# 7. Display previous chat messages
# --------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown("### 👤 User")
        else:
            st.markdown("### 🤖 AI PDF Chatbot")

        st.write(message["content"])

        if message.get("sources"):
            with st.expander("View Sources"):
                for source in message["sources"]:
                    st.markdown(source)
                    st.divider()


# --------------------------------------------------
# 8. Chat input
# --------------------------------------------------
question = st.chat_input(
    "Ask a question about your PDF..."
)

if question:
    if not st.session_state.pdf_processed:
        st.warning(
            "Please upload and process a PDF before "
            "asking questions."
        )

    elif st.session_state.vector_store is None:
        st.error(
            "The vector database is unavailable. "
            "Please process the PDF again."
        )

    else:
        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        # Display user message
        with st.chat_message("user"):
            st.markdown("### 👤 User")
            st.write(question)

        # Generate RAG answer
        with st.chat_message("assistant"):
            st.markdown("### 🤖 AI PDF Chatbot")

            try:
                with st.spinner(
                    "Searching the PDF and generating an answer..."
                ):
                    answer, source_documents = ask_question(
                        vector_store=st.session_state.vector_store,
                        question=question,
                        top_k=4,
                    )

                st.write(answer)

                source_list = []
                seen_sources = set()

                for document in source_documents:
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

                    source_key = (
                        source,
                        page,
                        chunk_id,
                    )

                    if source_key in seen_sources:
                        continue

                    seen_sources.add(source_key)

                    preview = document.page_content[:500]

                    source_text = (
                        f"**{source} — Page {page} — "
                        f"Chunk {chunk_id}**\n\n"
                        f"> {preview}..."
                    )

                    source_list.append(source_text)

                with st.expander("View Sources"):
                    for source_text in source_list:
                        st.markdown(source_text)
                        st.divider()

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": source_list,
                    }
                )

            except Exception as error:
                st.error(
                    f"Unable to generate an answer: {error}"
                )