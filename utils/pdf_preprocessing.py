from PyPDF2 import PdfReader
from utils.ocr import extract_text_from_images_in_pdf

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file, including text from images.

    This function reads a PDF file, extracts text from each page,
    and also extracts text from images within the PDF.

    Args:
    pdf_path (str): The path to the PDF file.

    Returns:
    tuple: A tuple containing three elements:
        - str: The extracted text from all pages combined.
        - str: The extracted text from images in the PDF.
        - list: A list of tuples, each containing a page number and its text.
    
    If an error occurs, it returns empty strings for text and image text,
    and an empty list for page texts.
    """
    try:
        with open(pdf_path, 'rb') as file:
            # Create a PdfReader object
            pdf_reader = PdfReader(file)
            
            text = ""  # To store all extracted text
            page_texts = []  # To store text from each page separately
            
            # Iterate through each page in the PDF
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text:
                    # Add page text to the overall text
                    text += page_text + "\n"
                    # Store page number and text
                    page_texts.append((page_num + 1, page_text))
            
            # Extract text from images in the PDF
            images_text = extract_text_from_images_in_pdf(pdf_path)
            
            return text, images_text, page_texts
    
    except Exception as e:
        # If an error occurs, print it and return empty results
        print(f"Error extracting text from PDF '{pdf_path}': {e}")
        return "", "", []
