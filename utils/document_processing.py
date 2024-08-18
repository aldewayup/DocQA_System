import os
import json
import time
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from utils.pdf_processing import extract_text_from_pdf

def process_single_document(file_name, documents_path):
    """
    Process a single PDF document.

    Args:
    file_name (str): Name of the PDF file to process.
    documents_path (str): Path to the directory containing the PDF files.

    Returns:
    dict: A dictionary containing extracted text and metadata, or None if processing fails.
    """
    try:
        # Construct the full path to the PDF file
        pdf_path = os.path.join(documents_path, file_name)
        # Extract text and images from the PDF
        text, images_text, page_texts = extract_text_from_pdf(pdf_path)
        # Return a dictionary with the extracted information
        return {
            'file_name': file_name,
            'text': text,
            'images_text': images_text,
            'page_texts': page_texts
        }
    except Exception as e:
        print(f"Error processing document '{file_name}': {e}")
        return None

def save_processed_documents(documents, output_file):
    """
    Save processed documents to a JSON file.

    Args:
    documents (list): List of processed document dictionaries.
    output_file (str): Path to the output JSON file.
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(documents, f)
    except Exception as e:
        print(f"Error saving processed documents to '{output_file}': {e}")

def load_processed_documents(output_file):
    """
    Load processed documents from a JSON file.

    Args:
    output_file (str): Path to the JSON file containing processed documents.

    Returns:
    list: List of processed document dictionaries, or None if loading fails.
    """
    try:
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading processed documents from '{output_file}': {e}")
    return None

def process_documents(documents_path, output_file):
    """
    Process multiple PDF documents in parallel.

    Args:
    documents_path (str): Path to the directory containing PDF files.
    output_file (str): Path to the output JSON file for saving processed documents.

    Returns:
    list: List of processed document dictionaries.
    """
    # Try to load previously processed documents
    documents = load_processed_documents(output_file)
    if documents is not None:
        print("Loaded processed documents from file.")
        return documents

    documents = []
    # Get a list of all PDF files in the specified directory
    pdf_files = [file_name for file_name in os.listdir(documents_path) if file_name.endswith('.pdf')]
    print(f"Found {len(pdf_files)} PDF documents to process.")
    start_time = time.time()

    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor() as executor:
        # Submit all tasks to the executor
        futures = {executor.submit(process_single_document, file_name, documents_path): file_name for file_name in pdf_files}
        # Process completed tasks with a progress bar
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing Documents"):
            file_name = futures[future]
            try:
                result = future.result()
                if result:
                    documents.append(result)
                    print(f"Successfully processed: {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    elapsed_time = time.time() - start_time
    print(f"Processing completed in {elapsed_time:.2f} seconds.")
    # Save the processed documents to a file
    save_processed_documents(documents, output_file)
    return documents
