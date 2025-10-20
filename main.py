from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# Assuming your config file and structure is now:
from email_query.config import OPENAI_API_KEY, CHROMA_DIR


# --- 1. Data Preparation ---

def make_docs(emails_content: list[str]) -> list[Document]:
    """Converts email text content into LangChain Document objects."""
    # Ensure correct document class is used for the modern core
    return [Document(page_content=text) for text in emails_content]


# --- 2. Vector Store Management ---

def store_in_vector_db(documents: list[Document]) -> Chroma:
    """
    Creates a Chroma vector database from the documents.
    Note: Manual persistence (db.persist) is no longer required with recent Chroma versions.
    """
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    
    # Create the vector store
    db = Chroma.from_documents(
        documents, embeddings, persist_directory=CHROMA_DIR
    )
    # Removed: db.persist() to eliminate deprecation warning
    
    print(f"✅ Chroma DB created/loaded at: {CHROMA_DIR}")
    return db


# --- 3. RAG Chain Construction ---

def build_qa_chain(db: Chroma):
    """
    Builds a modern RAG (Retrieval-Augmented Generation) chain using LCEL.

    Args:
        db: The Chroma vector store instance.

    Returns:
        A Runnable chain that takes a query and returns a response dictionary.
    """
    # 3.1. Define Retriever
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # 3.2. Define Prompt Template
    template = """
    You are an AI assistant specialized in answering questions based on email context. 
    Use the following retrieved email snippets as context to answer the user's question. 
    If you cannot find the answer within the context provided, you must state that 
    the information is not available in the emails.

    CONTEXT:
    {context}

    QUESTION: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 3.3. Define LLM
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        api_key=OPENAI_API_KEY
    )

    # 3.4. Create a formatting function for the retrieved documents
    def format_docs(docs):
        # Joins the page content of the documents into a single string for the prompt context
        return "\n\n---\n\n".join(doc.page_content for doc in docs)

    # 3.5. Build the RAG Chain using LCEL (LangChain Expression Language)
    # The chain flow:
    # 1. RunnablePassthrough: Takes the user query (as 'question').
    # 2. Retriever: Gets the documents.
    # 3. Format Docs: Formats documents into a single context string.
    # 4. Prompt | LLM: The context is then passed to the prompt and invoked with the LLM.
    
    rag_chain = (
        {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 3.6. Create a simple wrapper function to match the old structure
    # This function is what your app will call
    def qa_function(query):
        # We need to run the retriever separately to get the source documents for the output
        docs = retriever.invoke(query)
        answer = rag_chain.invoke(query)
        
        return {
            "answer": answer,
            "source_documents": docs
        }

    return qa_function