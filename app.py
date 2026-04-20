import streamlit as st
import time
from src.helper import get_pdf_text, get_text_chunks, get_vectorstore, get_conversation_chain

def user_input(user_question):
    if st.session_state.conversation is None:
        st.error("Please upload and process a document first.")
        return
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chat_history']

    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:
            st.write("User: ", message.content)
        else:
            st.write("Reply: ", message.content)

def main():
    st.title("IRS - Information Retrieval System")
    st.write("Welcome to the Information Retrieval System (IRS)!")

    user_question = st.text_input("Ask a question about the document:")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None

    if user_question:
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