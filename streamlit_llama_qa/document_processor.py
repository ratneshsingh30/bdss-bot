import os
from typing import List, Dict, Any, Tuple, Optional

class DocumentProcessor:
    """
    Class to process different document types and extract text.
    """
    
    @staticmethod
    def process_document(file_path: str, file_name: str) -> Tuple[str, Dict[str, Any]]:
        """
        Process a document file and extract text based on file type.
        
        Args:
            file_path: Path to the document file
            file_name: Original name of the file
            
        Returns:
            Tuple containing (extracted_text, metadata)
        """
        _, ext = os.path.splitext(file_name.lower())
        
        if ext in ['.txt', '.md']:
            return DocumentProcessor.process_text(file_path, file_name)
        else:
            # For now, handle all files as text files since we don't have PDF and PPT libraries
            return DocumentProcessor.process_text(file_path, file_name, ext[1:])
    
    @staticmethod
    def process_text(file_path: str, file_name: str, file_type: str = "text") -> Tuple[str, Dict[str, Any]]:
        """
        Extract text from a plain text file.
        
        Args:
            file_path: Path to the text file
            file_name: Original name of the file
            file_type: Type of file (for metadata)
            
        Returns:
            Tuple containing (extracted_text, metadata)
        """
        text = ""
        metadata = {
            "file_name": file_name,
            "file_type": file_type,
            "size": 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                metadata["size"] = len(text)
                
        except UnicodeDecodeError:
            # Try with different encodings if utf-8 fails
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    text = file.read()
                    metadata["size"] = len(text)
            except Exception as e:
                raise Exception(f"Error processing text file: {str(e)}")
                
        except Exception as e:
            raise Exception(f"Error processing text file: {str(e)}")
            
        return text.strip(), metadata
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into overlapping chunks for processing.
        
        Args:
            text: The text to split into chunks
            chunk_size: Maximum size of each chunk
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        
        if len(text) <= chunk_size:
            chunks.append(text)
        else:
            start = 0
            while start < len(text):
                end = min(start + chunk_size, len(text))
                
                # Adjust end to avoid cutting words
                if end < len(text):
                    # Try to find the nearest space
                    while end > start and text[end] != ' ':
                        end -= 1
                        
                chunks.append(text[start:end])
                start = end - overlap
                
                # Ensure we're not stuck
                if start >= end:
                    start = end
                    
        return chunks