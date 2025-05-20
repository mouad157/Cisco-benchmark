import re
import nltk
import pdfplumber
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure required NLTK data is downloaded
nltk.download('stopwords')
nltk.download('punkt_tab')
stpwrd = stopwords.words('english')

def pdf_to_text(file_path):
    """
    Extracts text from a PDF file, cleaning and returning both the combined text and individual pages.
    
    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        tuple: Cleaned full text and a list of text from individual pages.
    """
    with pdfplumber.open(file_path) as pdf:
        total_text = ""
        pages_text = []

        for page in pdf.pages:
            # Extract text within a specific bounding box
            #  .within_bbox((0, page.height * 0.18, page.width, page.height - page.height * 0.18))
            page_text = page.extract_text(layout=True) or ""
            pages_text.append(page_text)
            total_text += page_text

    # Clean text by normalizing spaces and newlines
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', re.sub(r' +', ' ', total_text))
    return cleaned_text, pages_text


def wizard_chunker(texts, chunk_size=300):
    """
    Processes a given text into chunks based on sentence content and a minimum chunk size.

    Args:
        texts (str): The input text to process.
        chunk_size (int): Minimum number of tokens in a chunk.

    Returns:
        list: List of text chunks.
    """
    chunks = []
    current_chunk = []
    sentences = texts.split("\n")
    
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        if not tokens:
            current_chunk.append(sentence)
            continue

        # Filter out stopwords and check if words qualify
        filtered_words = [word for word in tokens if word not in stpwrd]
        if len(filtered_words) > 1 and all(word[0].isupper() or word[0].isdigit() for word in filtered_words):
            # Add sentence to the current chunk
            if sum(len(word_tokenize(sent)) for sent in current_chunk) >= chunk_size:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
            current_chunk.append(sentence)
            
        else:
            current_chunk.append(sentence)
    
    # Append any remaining chunk
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    
    return chunks

