import streamlit as st
import time
from src.helper import get_pdf_text, get_text_chunks, get_vectorstore, get_conversation_chain

def user_input(user_question):
    if st.session_state.conversation is None:
        st.error("Please upload and process a document first.")
        return
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response.get('chat_history', [])

    # Display chat messages
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.chat_message("user").write(message.content)
        else:
            st.chat_message("assistant").write(message.content)

    # Show sources in expandable section
    if "source_documents" in response:
        with st.expander("📄 Sources"):
            for i, doc in enumerate(response["source_documents"]):
                page = doc.metadata.get("page", "N/A")
                
                st.markdown(f"**Source {i+1} (Page {page})**")
                st.write(doc.page_content[:300] + "...")
                st.divider()

def main():
    st.title("IRS - Information Retrieval System")
    st.write("Welcome to the Information Retrieval System (IRS)!")

    user_question = st.chat_input("Ask a question about the document:")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if user_question:
        if st.session_state.conversation is None:
            st.error("Please upload and process a document first.")
        else:
            user_input(user_question)

    with st.sidebar:
        st.header("Navigation")
        pdf_document = st.file_uploader("Upload a PDF document", type=["pdf"], accept_multiple_files=True)
        if st.button("Process Document"):
            if pdf_document:
                with st.spinner("Processing document..."):
                    
                    raw_text = get_pdf_text(pdf_document)
                    text_chunks = get_text_chunks(raw_text)
                    vector_store = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vector_store)

                    st.success("Document Scanned successfully!")
                    
                # Here you can add code to process the PDF document and extract information
            else:
                st.error("Please upload a PDF document to proceed.")

if __name__ == "__main__":
    main()