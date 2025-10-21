import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import io

def extract_text(file) -> str:
    """
    Extract text from uploaded file (PDF or image)
    """
    
    file_type = file.type
    
    if 'pdf' in file_type:
        return extract_text_from_pdf(file)
    elif 'image' in file_type:
        return extract_text_from_image(file)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def extract_text_from_pdf(file) -> str:
    """
    Extract text from PDF using PyMuPDF
    """
    try:
        # Read file bytes
        pdf_bytes = file.read()
        
        # Open PDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        
        doc.close()
        
        # If no text extracted, try OCR on images
        if len(text.strip()) < 50:
            return extract_text_from_pdf_with_ocr(pdf_bytes)
        
        return text.strip()
        
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def extract_text_from_pdf_with_ocr(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF using OCR (for scanned PDFs)
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Convert page to image
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
            img_bytes = pix.tobytes("png")
            
            # OCR the image
            image = Image.open(io.BytesIO(img_bytes))
            page_text = pytesseract.image_to_string(image)
            text += page_text + "\n"
        
        doc.close()
        return text.strip()
        
    except Exception as e:
        print(f"Error in PDF OCR: {e}")
        return ""


def extract_text_from_image(file) -> str:
    """
    Extract text from image using Tesseract OCR
    """
    try:
        # Open image
        image = Image.open(file)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Perform OCR
        text = pytesseract.image_to_string(image, config='--psm 6')
        
        return text.strip()
        
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess image for better OCR results
    (Optional enhancement)
    """
    from PIL import ImageEnhance, ImageFilter
    
    # Convert to grayscale
    image = image.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    
    # Sharpen
    image = image.filter(ImageFilter.SHARPEN)
    
    return image