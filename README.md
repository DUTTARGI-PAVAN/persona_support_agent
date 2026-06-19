# Persona-Adaptive Support Agent with RAG

## Overview

This project implements a Persona-Adaptive Customer Support Agent powered by Retrieval-Augmented Generation (RAG).

The system retrieves relevant information from a knowledge base, identifies the customer's persona, generates an adaptive response, and determines whether escalation to a human agent is required.

The solution demonstrates the practical use of AI concepts such as document chunking, vector embeddings, semantic search, persona classification, and intelligent response generation.


## Features
### Knowledge Base Processing

* Supports TXT, Markdown, and PDF documents.
* Automatically loads support documentation from the data folder.
* Splits documents into smaller chunks for efficient retrieval.

### Retrieval-Augmented Generation (RAG)

* Converts document chunks into vector embeddings.
* Stores embeddings in ChromaDB.
* Retrieves the most relevant chunks based on semantic similarity.

### Persona Classification

The system identifies customer personas:

* Technical Expert
* Frustrated User
* Business Executive

A rule-based classifier is used as a fallback mechanism due Gemini API quota limitations during development.

### Adaptive Response Generation:

Responses are customized according to the detected persona.

#### Technical Expert:

Provides detailed technical explanations and troubleshooting guidance.

#### Frustrated User:

Provides empathetic and easy-to-follow support instructions.

#### Business Executive:

Provides concise summaries and business-focused information.

### Escalation Detection:

The system automatically flags cases requiring human intervention:

* Billing disputes
* Refund requests
* Legal concerns
* Low-confidence classifications

### User Interface

A Streamlit-based web application provides an interactive user experience.

---

## Project Architecture

User Query

↓

Persona Classification

↓

RAG Retrieval

↓

Response Generation

↓

Escalation Decision

↓

Final Response

---

## Project Structure

persona-support-agent/
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── data/
│ ├── api_troubleshooting.md
│ ├── billing_policy.txt
│ ├── login_issues.txt
│ ├── account_recovery.txt
│ ├── subscription_management.txt
│ └── password_reset_guide.pdf
│
├── chroma_db/
└── src/
├── **init**.py
├── config.py
├── rag_pipeline.py
├── classifier.py
├── generator.py
└── escalator.py

---

## Technologies Used

### AI & NLP

* Sentence Transformers
* Retrieval-Augmented Generation (RAG)

### Vector Database

* ChromaDB

### Frameworks

* Streamlit

### Document Processing

* LangChain Text Splitters
* PyPDF

### Configuration

* Python Dotenv

---

## Core Concepts

### 1. Chunking

Large documents are split into smaller chunks before embedding generation.

Benefits:

* Better retrieval accuracy
* Reduced context size
* Improved semantic search

### 2. Embeddings

Text chunks are converted into numerical vector representations using the Sentence Transformer model:

all-MiniLM-L6-v2

Embeddings capture semantic meaning rather than exact keyword matches.

### 3. Vector Database

ChromaDB stores document embeddings and performs similarity search to retrieve relevant information.

### 4. Retrieval-Augmented Generation (RAG)

Instead of relying solely on a language model, the system first retrieves relevant information from the knowledge base and then generates responses using that information.

Benefits:

* More accurate answers
* Reduced hallucinations
* Domain-specific knowledge support

### 5. Persona-Adaptive Responses

The system modifies communication style according to the user's persona.

Examples:

Technical Expert:
Detailed technical guidance.

Frustrated User:
Empathetic and simplified instructions.

Business Executive:
High-level summaries and impact-focused explanations.

### 6. Escalation Logic

The system identifies situations where automated support may not be sufficient and recommends human intervention.

---

## Installation

### Clone Repository

git clone <repository-url>

cd persona-support-agent

### Create Virtual Environment

python -m venv venv

### Activate Environment

Windows:

venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

---

## Configuration

Create a .env file:

GEMINI_API_KEY=your_api_key_here

Note:
Gemini integration was planned for persona classification and response generation. Due to API quota restrictions during development, a rule-based fallback classifier was implemented.

---

## Build Knowledge Base

Run:

python src/rag_pipeline.py

Expected Output:

Loaded 6 documents

Created 15 chunks

Documents stored in ChromaDB

---

## Run Application

python -m streamlit run app.py

---

## Example Queries

### Technical Expert

My API returns a 401 unauthorized error.

### Frustrated User

Nothing works. I have been trying for hours.

### Business Executive

What is the impact of cancelling a subscription?

### Escalation Example

I was charged twice and need a refund.

---

## Future Improvements

* Full Gemini-powered persona classification
* LLM-based adaptive response generation
* Conversation memory
* Multi-language support
* Support ticket creation
* Deployment on cloud infrastructure

---

## Author

Pavan Duttargi

AI-Powered Persona Adaptive Support Agent Assignment
