import cv2
import numpy as np
import pytesseract

def preprocess_image(image):
    """
    Preprocess an image for OCR (Optical Character Recognition).

    This function applies several image processing techniques to enhance
    the image for better text recognition.

    Args:
    image (numpy.ndarray): The input image in BGR color format.

    Returns:
    numpy.ndarray: The preprocessed image ready for OCR.
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply binary thresholding
    # This creates a black and white image where text is white and background is black
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)
    
    return thresh

def extract_text_from_images_in_pdf(pdf_path):
    """
    Extract text from images in a PDF file.

    This function converts each page of a PDF to an image,
    preprocesses the image, and then applies OCR to extract text.

    Args:
    pdf_path (str): The path to the PDF file.

    Returns:
    str: The extracted text from all images in the PDF, or an empty string if an error occurs.
    """
    from pdf2image import convert_from_path
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        images_text = []
        
        for image in images:
            # Convert PIL Image to OpenCV format
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Preprocess the image
            preprocessed_image = preprocess_image(image_cv)
            
            # Configure Tesseract OCR
            custom_config = r'--oem 1 --psm 6'
            
            # Perform OCR on the preprocessed image
            image_text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
            
            # Add the extracted text to the list
            images_text.append(image_text.strip())
        
        # Join all extracted text into a single string
        return " ".join(images_text)
    except Exception as e:
        print(f"Error extracting text from images in PDF '{pdf_path}': {e}")
        return ""
