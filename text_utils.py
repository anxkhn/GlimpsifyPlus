import re

def clean_text(text: str) -> str: 
    # Replace multiple whitespaces with a single space
    
    # Remove punctuation and special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    text = text.lower()
    
    return text