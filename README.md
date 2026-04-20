# 🧠 IRS: AI-Powered PDF Question Answering with Retrieval-Augmented Generation

[![Live Demo](https://img.shields.io/badge/Live-Demo-green?style=for-the-badge&logo=streamlit)](https://irs-ai-assistant.streamlit.app/)

**An intelligent Document Q&A system leveraging RAG, vector embeddings, and Large Language Models to extract contextual answers from PDF documents.**

**⚡ Fully deployed and accessible via Streamlit Cloud**


## 🚀 Overview

IRS (Information Retrieval System) is a **Retrieval-Augmented Generation (RAG)** powered application that enables natural language question-answering over PDF documents. Instead of relying solely on an LLM's parametric knowledge, IRS combines the power of semantic search with generative AI to provide:

- **Accurate, context-grounded answers** derived directly from your documents
- **Transparent source attribution** showing which parts of the document were used
- **Conversational memory** maintaining context across multiple questions
- **Low hallucination risk** by constraining the LLM to document-provided context

### How RAG Works

Traditional LLMs are trained on static data and can "hallucinate" (generate plausible but incorrect information). RAG solves this by:

1. **Retrieving** relevant document chunks using semantic similarity search
2. **Augmenting** the LLM's prompt with this retrieved context
3. **Generating** answers grounded in actual document content

The result: Your LLM becomes a powerful search-and-answer agent with access to your proprietary documents, answering with factual precision.

---

## 🧠 How It Works: The RAG Pipeline

IRS implements a sophisticated **5-stage RAG architecture**:

### Stage 1️⃣: **PDF Ingestion & Text Extraction**
```
User uploads PDF → PyPDFLoader extracts text + metadata (page numbers)
```
- Handles multiple PDFs simultaneously
- Preserves document structure and page information for traceability

### Stage 2️⃣: **Intelligent Text Chunking**
```
Raw text → RecursiveCharacterTextSplitter → Semantic chunks (1000 tokens, 200 token overlap)
```
- **Chunk size: 1000 tokens** — balances context window and precision
- **Overlap: 200 tokens** — preserves semantic continuity across boundaries
- Recursive splitting respects natural document boundaries (paragraphs, sentences)

### Stage 3️⃣: **Embedding Generation**
```
Text chunks → HuggingFace Embeddings (all-MiniLM-L6-v2) → Dense vectors (384-dim)
```
- **Model**: `all-MiniLM-L6-v2` — lightweight, fast, production-grade sentence transformer
- Converts text into high-dimensional vectors capturing semantic meaning
- Enables similarity-based retrieval in vector space

### Stage 4️⃣: **Vector Database Indexing**
```
Embeddings → FAISS (Facebook AI Similarity Search) → Efficient vector index
```
- **FAISS**: Nearest-neighbor search in milliseconds
- Stores 384-dimensional embeddings for similarity-based retrieval
- Enables real-time document search at scale

### Stage 5️⃣: **Retrieval & LLM Augmentation**
```
User Question → Embedding → Similarity Search (k=5) → Top-5 Chunks + Question → LLaMA 3 → Answer
```
- Retrieves **top-5 most relevant chunks** (similarity search)
- Constructs augmented prompt: `[Context] + [Question]`
- LLaMA 3 (8B, via OpenRouter) generates grounded answer
- **Conversation Memory**: Maintains chat history for context-aware follow-ups

---

## ⚙️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | [LangChain](https://python.langchain.com) | Orchestrates RAG pipeline & LLM chains |
| **Vector DB** | [FAISS](https://github.com/facebookresearch/faiss) | Efficient semantic similarity search |
| **Embeddings** | [HuggingFace](https://huggingface.co) (all-MiniLM-L6-v2) | Text-to-vector conversion |
| **LLM** | [LLaMA 3 8B](https://huggingface.co/meta-llama) | Answer generation |
| **UI** | [Streamlit](https://streamlit.io) | Interactive web interface |
| **PDF Processing** | [PyPDF](https://pypi.org/project/pypdf/) | Document text extraction |
| **Memory** | LangChain ConversationBufferMemory | Chat history management |

---

## ✨ Features

- **📄 Multi-PDF Upload**: Process multiple documents in a single session
- **🔍 Semantic Search**: Retrieve contextually relevant document sections
- **💬 Conversational QA**: Ask follow-up questions with maintained context
- **📌 Source Attribution**: View exact document sources (page numbers & text snippets)
- **⚡ Real-time Processing**: Stream answers as they're generated
- **🧠 No Hallucinations**: Answers constrained to document content
- **💾 Chat History**: Track conversation flow and previous questions

---

## 📂 Project Structure

```
IRS/
├── app.py                          # Streamlit frontend & main entry point
├── src/
│   ├── __init__.py
│   └── helper.py                   # RAG pipeline implementation
├── requirements.txt                # Python dependencies
├── setup.py                        # Package configuration
├── .env.example                    # API key template
└── README.md                       # This file
```

### Key Files Explained

**`app.py`** — Streamlit Web Interface
- PDF upload widget with multi-file support
- Document processing trigger with spinner feedback
- Chat interface with message history display
- Expandable sources panel showing document citations

**`src/helper.py`** — RAG Pipeline Core
- `get_pdf_text()` — Extract text from PDFs with metadata preservation
- `get_text_chunks()` — Split documents into semantic chunks
- `get_vectorstore()` — Initialize FAISS embeddings & indexing
- `get_conversation_chain()` — Setup LLM + retriever + memory chain

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+
- OpenRouter API key (free tier available)

### Step 1: Clone Repository
```bash
git clone https://github.com/Akshat5249/IRS.git
cd IRS
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key
Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:
```
API_KEY=your_api_key_here
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🌐 Deployment

### Deploy on Streamlit Cloud (Recommended)
1. Push your repo to GitHub
2. Connect repo at [share.streamlit.io](https://share.streamlit.io)
3. Add `API_KEY` as a secret in Streamlit Cloud settings
4. Deploy with one click — automatic updates on push

### Deploy on Other Platforms
- **Hugging Face Spaces**: Free GPU, same Streamlit deployment process
- **Railway/Render**: Traditional containerized deployment
- **AWS/GCP**: For production-grade scaling

---

## 🧪 Example Queries

Once you've uploaded a PDF, try these types of questions:

1. **Direct Factual Questions**
   - "What is the main conclusion of this document?"
   - "List all the key metrics mentioned."

2. **Comparative Questions**
   - "Compare the approaches mentioned in sections A and B."
   - "What are the differences between the two methods?"

3. **Analytical Questions**
   - "Why did the author make this decision?"
   - "What are the implications of this finding?"

4. **Summarization Requests**
   - "Summarize the methodology section."
   - "What are the limitations of this approach?"

5. **Context-Dependent Follow-ups**
   - "Can you explain that in simpler terms?"
   - "How does this relate to what you said earlier?"

---

## 🔥 Future Improvements

- **Answer Highlighting**: Visual emphasis on the retrieved context within source documents
- **Multi-Modal Documents**: Support for images, tables, and scanned PDFs (OCR)
- **Advanced Chunking**: Semantic chunking based on document structure
- **Reranking**: Cross-encoder reranking to improve retrieval quality
- **Caching**: Redis-backed cache for repeated queries
- **User Authentication**: Multi-user support with document management
- **Hybrid Search**: Combine semantic search with keyword-based BM25 retrieval
- **Custom Prompts**: User-configurable system prompts for domain-specific QA
- **Export Functionality**: Save conversations and citations as PDF/Word

---

## 🧠 Key AI Concepts Explained

### **Retrieval-Augmented Generation (RAG)**
RAG bridges the gap between LLM knowledge and up-to-date, proprietary information by retrieving relevant context before generation. It dramatically reduces hallucinations and improves factual accuracy.

**Formula**: *Answer = LLM(Document Context + Question)*

### **Embeddings**
Text embeddings convert words/sentences into numerical vectors in high-dimensional space. Semantic similarity corresponds to vector proximity—similar sentences have similar embeddings. This enables semantic search without keyword matching.

**Use Case**: Find document sections relevant to a user's question, even with different wording.

### **Vector Databases (FAISS)**
Traditional databases index text by keywords. Vector databases index by semantic meaning, enabling ultra-fast similarity search. FAISS uses Approximate Nearest Neighbor (ANN) algorithms for sub-millisecond retrieval.

**Why FAISS?**: Optimized for semantic search at production scale (millions of vectors).

### **Prompt Augmentation**
Instead of asking an LLM a question directly, we construct a "augmented prompt" containing:
```
[Retrieved Document Context] + [User Question]
```
This constraints the LLM to answer based only on provided information, eliminating hallucinations.

### **Semantic Chunking**
Breaking documents into overlapping chunks (not random splits) preserves semantic cohesion. Overlapping regions maintain context continuity across chunk boundaries.

**Optimal Chunk Size**: 1000 tokens ≈ 750 words (balances context & precision)

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Contact & Support

Have questions? Open an issue on GitHub or reach out directly.

- **Email**: akshattayal5249@gmail.com
- **Linkedin**: [Akshat Tayal](https://www.linkedin.com/in/akshattayal/)

---

## 🎓 Learn More

- [LangChain Documentation](https://python.langchain.com)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [HuggingFace Embeddings](https://huggingface.co/sentence-transformers)
- [LLaMA 3 Model Card](https://huggingface.co/meta-llama/Llama-3-8b)
- [OpenRouter API Docs](https://openrouter.ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io)

---

Thank You ❤️
