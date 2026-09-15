# Microsoft Foundry Document Intelligence

AI-powered document analysis API built with **FastAPI** and **Microsoft Foundry**.

The application accepts PDF, TXT, and Markdown documents, extracts their text, and uses **GPT-4.1-mini** to analyze the document and return structured information.

## Features

* PDF, TXT, and Markdown document support
* Text extraction from uploaded documents
* LLM-based document analysis
* Structured JSON output using Pydantic
* Entity and financial value extraction
* Missing information and risk detection
* Prompt injection protection
* File type and size validation
* AI evaluation tests
* REST API with FastAPI
* Docker support

## Architecture

```text
Document
   ↓
FastAPI
   ↓
File Validation
   ↓
Text Extraction
   ↓
Prompt Engineering
   ↓
Microsoft Foundry
   ↓
GPT-4.1-mini
   ↓
Pydantic Validation
   ↓
Structured JSON
```

## Tech Stack

* Python
* FastAPI
* Microsoft Foundry
* GPT-4.1-mini
* Azure Identity
* Pydantic
* PyPDF
* Docker

## Project Structure

```text
.
├── app/
│   ├── document.py
│   ├── foundry.py
│   ├── logging_config.py
│   ├── main.py
│   ├── prompts.py
│   └── schemas.py
│
├── data/
│   └── sample.txt
│
├── evaluation/
│   ├── documents/
│   ├── run_evaluation.py
│   └── test_cases.json
│
├── test/
│   ├── test_ai.py
│   └── test_connection.py
│   └── test_document.py
├── .env
├── .gitignore
├── .dockerignore
├── Dockerfile
├── requirements.txt
```

## Setup

Clone the repository and install the dependencies:

```bash
git clone https://github.com/lukagobechia/RAG-based-AI-Assistant.git
cd microsoft-foundry-document-intelligence

python -m venv .venv
```

Activate the virtual environment.

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```env
FOUNDRY_PROJECT_ENDPOINT=your_foundry_project_endpoint
MODEL_DEPLOYMENT=document-intelligence
```

The application uses Azure authentication through `DefaultAzureCredential`.

Make sure you are authenticated with Azure before running the application:

```bash
az login
```

## Run the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://localhost:8000/docs
```

Upload a PDF, TXT, or Markdown file to:

```text
POST /analyze
```

## Example Response

```json
{
  "filename": "invoice.pdf",
  "analysis": {
    "document_type": "Invoice",
    "summary": "Invoice for software development services.",
    "entities": [
      {
        "role": "Company",
        "name": "ABC Technologies Ltd."
      }
    ],
    "dates": [
      "2026-09-15"
    ],
    "financial_values": [
      {
        "description": "Total amount due",
        "amount": 1250,
        "currency": "USD"
      }
    ],
    "risks": [
      "Invoice payment is currently unpaid."
    ],
    "missing_information": [
      "Payment method"
    ]
  }
}
```

## Evaluation

The project includes a small evaluation dataset covering:

* Document classification
* Entity extraction
* Financial value extraction
* Incomplete documents
* Prompt injection scenarios

Run the evaluation with:

```bash
python evaluation/run_evaluation.py
```

The evaluation reports accuracy for each category and the overall test suite.

## Security

The application includes basic AI and API security measures:

* Uploaded files are validated by type and size
* Documents are treated as untrusted data
* Prompt injection instructions inside documents are not followed
* System instructions and credentials are not exposed
* Internal errors are not returned to API users
* Document contents are not written to application logs

## Docker

Build the image:

```bash
docker build -t document-intelligence .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env document-intelligence
```

## Future Improvements

* More comprehensive evaluation datasets
* Better document parsing for complex PDFs
* Additional document types
* Performance and latency monitoring
* Automated evaluation pipeline
* Cloud deployment
