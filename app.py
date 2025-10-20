import streamlit as st
from datetime import date
from email_query.fetch_emails import fetch_emails_for_day
from main import make_docs, store_in_vector_db, build_qa_chain
from email_query.config import USER_PRINCIPAL_NAME

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Email Query App", 
    page_icon="📧", 
    layout="centered"
)
st.title("📧 Email Query App with LangChain")

st.markdown(f"""
This app fetches Outlook emails for **{USER_PRINCIPAL_NAME}** on a selected day, 
embeds them in a vector database, and lets you ask questions about their content.
""")

# --- Main App Logic ---

# Date selection
selected_date = st.date_input("Select a date to fetch emails from:", value=date.today())

# Button to trigger the email fetching and processing
if st.button("Fetch and Process Emails"):
    with st.spinner(f"Fetching emails for {selected_date}..."):
        try:
            # 1. Fetch emails
            emails = fetch_emails_for_day(str(selected_date))
            if not emails:
                st.warning("No emails found for the selected day. Please try another date.")
                st.stop()
            
            st.success(f"Successfully fetched {len(emails)} emails.")

            # 2. Convert emails to LangChain documents
            with st.spinner("Creating document embeddings..."):
                docs = make_docs(emails)
            
            # 3. Store documents in Chroma vector DB
            with st.spinner("Storing documents in vector database... This may take a moment."):
                db = store_in_vector_db(docs)
            
            # 4. Build the QA chain and store it in session state
            st.session_state.qa_chain = build_qa_chain(db)
            st.success("Emails have been processed! You can now ask questions.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- Query Section (appears only after processing) ---
if "qa_chain" in st.session_state:
    st.header("Ask a Question")
    
    query = st.text_input("Enter your question about the fetched emails:", placeholder="e.g., What was the main topic of the marketing update?")
    
    if st.button("Get Answer"):
        if query and query.strip():
            with st.spinner("Searching for the answer..."):
                try:
                    # Run the query through the QA function
                    result = st.session_state.qa_chain(query)
                    answer = result.get("answer")
                    
                    st.markdown("### Answer")
                    st.write(answer)

                    # Optionally, display source documents
                    with st.expander("Show source documents"):
                        source_docs = result.get("context", result.get("source_documents", []))
                        if source_docs:
                            for i, doc in enumerate(source_docs):
                                st.write(f"**Document {i+1}:**")
                                st.write(doc.page_content if hasattr(doc, 'page_content') else str(doc))
                                st.write("---")

                except Exception as e:
                    st.error(f"Failed to get an answer: {e}")
        else:
            st.warning("Please enter a question.")