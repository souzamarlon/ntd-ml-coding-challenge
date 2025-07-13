# Document AI Project - ntd-ml-coding-challenge

## Overview

This project processes scanned documents using OCR, extracts entities, and enables querying by similarity with embeddings powered by OpenAI.

## 🐳 Getting Started with Docker

### 1. Clone the repository

```bash
git clone https://github.com/souzamarlon/ntd-ml-coding-challenge.git
cd ntd-ml-coding-challenge/document_ai_project
```

## Setup and Running

### 1. Create a .env file

Create a .env file in the root directory with your OpenAI API key:

```bash
OPENAI_API_KEY="sk-yourtoken"
```

### 2. Build and start the Docker containers

```bash
docker-compose up --build
```

### 3. Add sample documents

To test document extraction and embedding, place your dataset files (e.g., images in JPG format) inside the `document_ai_project/documents/docs/` directory

### 4. Process the documents

Run the management command inside the Docker container to process and index the documents:

```bash
docker compose run --rm web python manage.py process_documents --path /data/docs

Output example:
{
	"document_type": "letter",
	"entities": "{\"document_type\": \"letter\", \"sender\": null, \"recipient\": \"Dr. Li\", \"dates\": [\"April 17\"], \"addresses\": [\"University of Minnesota, Minneapolis, Minnesota, 55455\"], \"amount\": null, \"other_metadata\": {\"hotel\": \"Holiday Inn on St. Anthony\", \"travel_details\": \"returning to Louisville on the afternoon of the 17th\", \"reference_number\": \"MuR/mja/322\", \"subject\": \"Particle size, University of Minnesota\"}}"
}
```

### 🧪 Running Tests

```bash
docker compose run --rm web pytest
```

### 🤖 API Endpoints

Example endpoint:

```bash
POST /api/upload/
Example:
curl --request POST \
  --url http://localhost:8000/api/upload/ \
  --header 'Content-Type: multipart/form-data; boundary=---011000010111000001101001' \
  --form 'file=@C:\Users\Marlon\docs-sm\advertisement\00005259.jpg'
```

📬 Contact

Built by Marlon — feel free to reach out for questions or feedback.
