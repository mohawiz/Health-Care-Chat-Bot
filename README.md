# 🩺 MediQuery: Healthcare Chatbot with Medical PDF RAG

A production-ready backend for a **Healthcare Chatbot** that leverages **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers from medical literature. It processes PDF documents, creates a searchable knowledge base, and uses a state-of-the-art LLM to generate informative responses about symptoms, treatments, and diseases.

## ✨ Core Features

- **📄 Intelligent PDF Processing**: Automatically loads and extracts text from medical PDFs in a specified directory.
- **🔍 Semantic Search Engine**: Splits text into optimal chunks and creates vector embeddings using the `all-MiniLM-L6-v2` model for precise information retrieval.
- **🗃️ Vector Database Management**: Stores and retrieves embeddings efficiently using **Pinecone**, enabling fast similarity search across large document collections.
- **🤖 Advanced Q&A with RAG**: Combines retrieved medical context with the powerful `llama3-70b-8192` model via **Groq API** to generate factual, cited responses.
- **⚙️ Customizable Pipeline**: Built with **LangChain** for modularity, allowing easy swaps of models, vector databases, or chunking strategies.
- **🎯 Specialization-Aware Design**: Prompt template structured to support future integration with specialist appointment booking (e.g., dermatology, cardiology).

## 🏗️ System Architecture & RAG Pipeline

```mermaid
graph TD
    A[Medical PDFs] --> B[PyPDFLoader];
    B --> C[Raw Text];
    C --> D[RecursiveCharacterTextSplitter];
    D --> E[Text Chunks];
    E --> F[Embedding Model<br/>all-MiniLM-L6-v2];
    F --> G[Vector Embeddings];
    G --> H[Pinecone Vector DB];
    
    I[User Query] --> J;
    H --> J[Semantic Search];
    J --> K[Top-K Relevant Chunks];
    K --> L[LLM Prompt + Context];
    L --> M[ChatGroq LLM<br/>llama3-70b-8192];
    M --> N[Factual, Context-Rich Answer];
