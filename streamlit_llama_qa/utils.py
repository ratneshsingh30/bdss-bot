import os
import tempfile
import uuid
from typing import List, Tuple, Dict, Any

def create_temp_file(uploaded_file, extension=None) -> Tuple[str, str]:
    """
    Create a temporary file from an uploaded file and return its path and name.
    
    Args:
        uploaded_file: The uploaded file from Streamlit
        extension: File extension to use (optional)
        
    Returns:
        Tuple containing (file_path, file_name)
    """
    if extension is None:
        # Extract extension from original filename
        _, ext = os.path.splitext(uploaded_file.name)
    else:
        ext = extension
        
    # Generate a unique filename
    unique_id = str(uuid.uuid4())
    temp_filename = f"{unique_id}{ext}"
    
    # Create a temporary file
    temp_path = os.path.join(tempfile.gettempdir(), temp_filename)
    
    # Write the uploaded file to the temporary file
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return temp_path, uploaded_file.name

def format_document_text(text: str, max_chars=100) -> str:
    """
    Format document text for display in the UI.
    
    Args:
        text: The document text to format
        max_chars: Maximum characters to show before truncating
        
    Returns:
        Formatted text string
    """
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text

def get_file_icon(file_name: str) -> str:
    """
    Get the appropriate icon for a file based on its extension.
    
    Args:
        file_name: The name of the file
        
    Returns:
        Icon string for the file type
    """
    _, ext = os.path.splitext(file_name.lower())
    
    if ext == ".pdf":
        return "📄"
    elif ext in [".ppt", ".pptx"]:
        return "📊"
    elif ext in [".txt", ".md", ".doc", ".docx"]:
        return "📝"
    else:
        return "📁"
