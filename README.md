# DocQA System

DocQA is an advanced document question-answering system that implements Retrieval-Augmented Generation (RAG) to process PDF documents, extract text (including from images), and answer user queries based on the document content.

DocQA is an advanced AI-driven document-based question answering system that efficiently extracts and processes information from diverse document formats, including PDFs and Standard Operating Procedures (SOPs) containing both text and images. This system leverages cutting-edge natural language processing and computer vision techniques to provide accurate answers to user queries, streamlining data retrieval processes and enhancing decision-making capabilities.

## Key Features

- AI-powered information extraction from text and images in PDF documents
- Retrieval-Augmented Generation (RAG) with optimizations:
  - Hybrid search mechanism combining dense and sparse retrieval methods
  - Document re-ranking using GPT models for enhanced relevance
  - Chunk-based processing for efficient handling of large documents
- Precise source attribution with document name and page number for each answer
- Efficient handling of large document sets through parallelization
- Semantic embedding and vector store creation for quick information retrieval
- OCR processing for text extraction from images within documents
- Text preprocessing and chunking for optimized indexing and searching
- User-friendly query interface with Excel output for easy result analysis
- Ability to process and answer queries based on both textual and graphical information
- Scalable architecture capable of handling diverse content types and document formats
- Optimized reprocessing to avoid redundant document analysis for subsequent queries
- Integration with OpenAI's GPT models for advanced natural language processing

## Requirements

- Python 3.7+
- OpenAI API key
- Tesseract OCR engine

## Installation

1. **Clone this repository:**

```
git clone https://github.com/yourusername/docqa-system.git
cd docqa-system
```

2. **Create and activate a virtual environment:**

On Windows
```
python -m venv venv
.\venv\Scripts\activate
```

On macOS and Linux

```
python3 -m venv venv
source venv/bin/activate
```

3. **Install the required Python packages:**

`
pip install -r requirements.txt
`

4. **Install Tesseract OCR engine. Follow the instructions for your operating system:**

- [Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- [macOS](https://tesseract-ocr.github.io/tessdoc/Installation.html)
- [Linux](https://tesseract-ocr.github.io/tessdoc/Installation.html)


5. **Create a `config.json` file in the root directory with the following content:**

```json
{
  "openai_api_key": "your-api-key-here",
  "tesseract_path": "/path/to/tesseract",
  "documents_path": "./documents/",
  "processed_documents_path": "./processed_documents.json",
  "output_excel_path": "./query_answers.xlsx",
  "gpt_model": "gpt-4"
}
```

- *Replace your-api-key-here with your actual OpenAI API key and adjust other paths as needed.*

6. **Usage:**

- Place your PDF documents in the documents folder (or the path specified in your config).

- Run the main script:

`
python main.py
`

- Follow the prompts to enter your queries. 
- Type 'done' when finished.
- The script will process your queries using RAG and save the results in an Excel file.

## Project Structure


```
DocQA-System/
│
├── main.py
│
├── requirements.txt
│
├── data/
│   ├── documents/
│       └── inputfiles.pdf
│   └── output_file.xlsx
│   
├── README.MD
│
└── utils/
    ├── config.py
    ├── document_processing.py
    ├── embedding.py
    ├── search.py
    ├── qa.py
    ├── excel.py
    └── ocr.py
```

- main.py: The main script that orchestrates the entire RAG process.
- utils/:
  - config.py: Functions for loading configuration and setting up Tesseract.
  - document_processing.py: Functions for processing PDF documents and extracting text.
  - embedding.py: Functions for creating the vector store for efficient retrieval.
  - search.py: Functions for performing hybrid search and re-ranking results.
  - qa.py: Functions for generating answers using RAG and finding relevant page numbers.
  - excel.py: Functions for saving results to an Excel file.
  - ocr.py: Functions for OCR processing of images in PDFs.