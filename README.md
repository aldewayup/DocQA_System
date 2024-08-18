# DocQA System

DocQA is an advanced document question-answering system that implements Retrieval-Augmented Generation (RAG) to process PDF documents, extract text (including from images), and answer user queries based on the document content.

## Key Features

- Retrieval-Augmented Generation (RAG) for accurate and context-aware answers
- RAG optimizations:
  - Hybrid search combining dense and sparse retrieval methods for improved document retrieval
  - Re-ranking of search results using GPT models to enhance relevance
  - Chunk-based processing for handling large documents efficiently
- PDF processing with text extraction from both textual content and images using OCR
- Vector store creation for efficient document searching and retrieval
- Question answering based on the most relevant document sections
- Source attribution with file name and page number for each answer
- Output of results to an Excel file for easy review and analysis

## Requirements

- Python 3.7+
- OpenAI API key
- Tesseract OCR engine

## Installation

1. Clone this repository:

git clone https://github.com/yourusername/docqa-system.git
cd docqa-system
text

2. Create and activate a virtual environment:

On Windows
python -m venv venv
.\venv\Scripts\activate
On macOS and Linux
python3 -m venv venv
source venv/bin/activate
text

3. Install the required Python packages:

pip install -r requirements.txt
text

4. Install Tesseract OCR engine. Follow the instructions for your operating system:
- [Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- [macOS](https://tesseract-ocr.github.io/tessdoc/Installation.html)
- [Linux](https://tesseract-ocr.github.io/tessdoc/Installation.html)

5. Create a `config.json` file in the root directory with the following content:
```json
{
  "openai_api_key": "your-api-key-here",
  "tesseract_path": "/path/to/tesseract",
  "documents_path": "./documents/",
  "processed_documents_path": "./processed_documents.json",
  "output_excel_path": "./query_answers.xlsx",
  "gpt_model": "gpt-4"
}

Replace your-api-key-here with your actual OpenAI API key and adjust other paths as needed.
Usage
Place your PDF documents in the documents folder (or the path specified in your config).
Run the main script:
text
python main.py

Follow the prompts to enter your queries. Type 'done' when finished.
The script will process your queries using RAG and save the results in an Excel file.
Project Structure
main.py: The main script that orchestrates the entire RAG process.
utils/:
config.py: Functions for loading configuration and setting up Tesseract.
document_processing.py: Functions for processing PDF documents and extracting text.
embedding.py: Functions for creating the vector store for efficient retrieval.
search.py: Functions for performing hybrid search and re-ranking results.
qa.py: Functions for generating answers using RAG and finding relevant page numbers.
excel.py: Functions for saving results to an Excel file.
ocr.py: Functions for OCR processing of images in PDFs.