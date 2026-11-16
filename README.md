
# Inventory Guidance Assistant

An AI-powered inventory management assistant that combines Agentic AI, Retrieval-Augmented Generation (RAG), LangGraph, and SQLite.

The application helps users understand inventory levels, identify low-stock products, calculate replenishment quantities, and retrieve inventory policies from an SOP document.

It also includes role-based stock approval and automatic audit logging.

## Features

- **AI Inventory Assistant:** Answers inventory-related questions using a locally running LLM.
- **Agentic AI:** Uses LangGraph to orchestrate inventory tools and language-model responses.
- **Retrieval-Augmented Generation:** Retrieves relevant information from an Inventory SOP PDF.
- **Semantic Search:** Uses Sentence Transformers and FAISS for document retrieval.
- **Inventory Management:** Retrieves stock levels, identifies low-stock products, and calculates replenishment recommendations.
- **Role-Based Authentication:** Supports administrator and regular employee accounts.
- **Approval Workflow:** Restricts stock updates to authorized administrators.
- **Audit Logging:** Records previous and new stock quantities, approver identity, and timestamps.
- **Streamlit Interface:** Provides an interactive application for users and administrators.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Large Language Model | Llama 3.1 8B |
| Local LLM Runtime | Ollama |
| Agent Framework | LangGraph |
| LLM Integration | LangChain |
| Embeddings | Sentence Transformers |
| Vector Database | FAISS |
| Relational Database | SQLite |
| PDF Processing | PyMuPDF |
| Authentication | Werkzeug Password Hashing |

## Architecture

### Inventory Question Answering

1. User submits an inventory-related question.
2. LangGraph coordinates the agent workflow.
3. The agent selects an appropriate inventory tool.
4. The tool retrieves information from SQLite or the SOP retrieval pipeline.
5. The agent returns a response.

### SOP Question Answering (RAG)

1. Read the Inventory SOP PDF using PyMuPDF.
2. Split document text into smaller chunks.
3. Generate embeddings using Sentence Transformers.
4. Store embeddings in a FAISS vector index.
5. Retrieve relevant chunks using semantic similarity.
6. Use the local Llama model to generate a context-grounded response.

### Stock Approval Workflow

1. User selects a product and proposes a stock change.
2. The application displays the current and proposed quantities.
3. Administrator authorization is checked against SQLite.
4. Authorized stock changes are saved.
5. An audit record is created in the same database transaction.
6. Administrators can review the stock audit history.

## Project Setup

### Prerequisites

- Python 3.10 or later
- Ollama installed
- Git


### 1. Clone the repository

git clone https://github.com/Pratiksha-ML/inventory-guidance-assistant.git

cd inventory-guidance-assistant

### 2. Create a virtual environment

python -m venv .venv

### 3. Install dependencies

pip install -r requirements.txt


### 4. Download the local LLM

```bash
ollama pull llama3.1:8b
```

### 5. Initialize the database

```bash
python database_setup.py
python insert_inventory.py
```

### 6. Create an administrator account

```bash
python create_admin.py
```

Optionally, create a regular employee account:

```bash
python create_regular_user.py
```

### 7. Start the application

```bash
streamlit run app.py
```

Open the local Streamlit URL displayed in your terminal.

## Testing

Run inventory unit tests:

```bash
python -m unittest test_inventory -v
```

Run agent tests:

```bash
python -m unittest test_agent -v
```

Run the employee authorization security test:

```bash
python test_employee_security.py
```

## Sample Inventory Dataset

The demonstration dataset contains:

| Product | Available Stock | Minimum Stock |
|---|---:|---:|
| Wireless Mouse | 15 | 25 |
| Keyboard | 50 | 20 |
| Monitor | 5 | 10 |

The application identifies low-stock products and calculates replenishment quantities based on minimum stock levels.

## Security Considerations

- Passwords are stored as hashes rather than plaintext.
- Stock approval requires administrator authorization.
- Authorization is checked against the database.
- Stock changes and audit entries are saved transactionally.

This is a local portfolio demonstration. Additional security controls would be required before production deployment.

## Future Enhancements

- FastAPI backend
- Cloud deployment
- Supplier management
- Purchase order generation
- Advanced inventory analytics
- Improved monitoring and evaluation
- Expanded automated test coverage

## Author

Developed as a hands-on AI/ML portfolio project.
