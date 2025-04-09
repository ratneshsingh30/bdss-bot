import streamlit as st
import os
import time
from typing import List, Dict, Any

from utils import create_temp_file, format_document_text, get_file_icon
from document_processor import DocumentProcessor
from embedding_handler import EmbeddingHandler
from llama_interface import LlamaInterface

# Initialize session state variables
if "embedding_handler" not in st.session_state:
    st.session_state.embedding_handler = EmbeddingHandler()
    
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Meta-Llama-4"  # Default model
    
if "llama_interface" not in st.session_state:
    st.session_state.llama_interface = LlamaInterface()
    
if "documents" not in st.session_state:
    st.session_state.documents = []
    
if "processing" not in st.session_state:
    st.session_state.processing = False
    
if "answer" not in st.session_state:
    st.session_state.answer = None
    
if "huggingface_api_key" not in st.session_state:
    st.session_state.huggingface_api_key = ""

def process_uploaded_file(uploaded_file):
    """Process an uploaded file and add it to the embedding handler."""
    with st.spinner(f"Processing {uploaded_file.name}..."):
        try:
            # Create a temporary file
            temp_path, file_name = create_temp_file(uploaded_file)
            
            # Extract text and metadata
            text, metadata = DocumentProcessor.process_document(temp_path, file_name)
            
            # Add to embeddings
            st.session_state.embedding_handler.add_document(text, metadata)
            
            # Add to document list
            st.session_state.documents.append({
                "name": file_name,
                "text": text[:200] + "..." if len(text) > 200 else text,
                "metadata": metadata
            })
            
            # Clean up temporary file
            try:
                os.remove(temp_path)
            except:
                pass
                
            return True
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return False
            
def generate_answer(question):
    """Generate an answer for the question using LLaMA 4."""
    with st.spinner("Generating answer..."):
        try:
            # Get relevant context from documents
            context = st.session_state.embedding_handler.get_context_for_query(question)
            
            # Generate answer using LLaMA 4
            response = st.session_state.llama_interface.generate_response(question, context)
            
            return response
            
        except Exception as e:
            st.error(f"Error generating answer: {str(e)}")
            return {
                "answer": f"Error: {str(e)}",
                "sources": [],
                "success": False
            }

# App layout and functionality
st.title("Document Q&A with LLaMA Models")
st.write("Upload documents and ask questions about their content using LLaMA models")

# Sidebar for file upload and management
with st.sidebar:
    st.header("Document Management")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload PDF, PPT, or TXT files",
        type=["pdf", "ppt", "pptx", "txt"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        # Process all uploaded files
        for uploaded_file in uploaded_files:
            # Check if this file is already processed
            if not any(doc["name"] == uploaded_file.name for doc in st.session_state.documents):
                process_uploaded_file(uploaded_file)
    
    # Document list
    st.subheader("Uploaded Documents")
    if not st.session_state.documents:
        st.info("No documents uploaded yet.")
    else:
        for i, doc in enumerate(st.session_state.documents):
            with st.expander(f"{get_file_icon(doc['name'])} {doc['name']}"):
                if doc["metadata"]["file_type"] == "pdf":
                    st.write(f"Pages: {doc['metadata']['pages']}")
                elif doc["metadata"]["file_type"] == "ppt":
                    st.write(f"Slides: {doc['metadata']['slides']}")
                elif doc["metadata"]["file_type"] == "text":
                    st.write(f"Size: {doc['metadata']['size']} characters")
                
                st.text_area(
                    "Preview:",
                    doc["text"],
                    height=100,
                    disabled=True
                )
                
                # Delete document button
                if st.button(f"Delete", key=f"delete_{i}"):
                    # This would require rebuilding the index, but for simplicity we'll just remove from the list
                    st.session_state.documents.pop(i)
                    st.rerun()

# API Key input and model selection
api_key_container = st.container()
with api_key_container:
    st.subheader("LLaMA Model Configuration")
    st.info("This application requires a Hugging Face API key to use the LLaMA models.", icon="ℹ️")
    
    # Model selection dropdown
    model_options = list(LlamaInterface.AVAILABLE_MODELS.keys())
    selected_model = st.selectbox(
        "Select LLaMA Model:",
        options=model_options,
        index=model_options.index(st.session_state.selected_model) if st.session_state.selected_model in model_options else 0,
        help="Choose the LLaMA model version to use for question answering."
    )
    
    # API key input 
    api_key = st.text_input(
        "Enter your Hugging Face API key:",
        type="password",
        value=st.session_state.huggingface_api_key,
        help="Get your API key from https://huggingface.co/settings/tokens"
    )
    
    # Check for changes and update
    if (api_key != st.session_state.huggingface_api_key or 
        selected_model != st.session_state.selected_model):
        
        st.session_state.huggingface_api_key = api_key
        st.session_state.selected_model = selected_model
        
        # Recreate the LLaMA interface with the new settings
        st.session_state.llama_interface = LlamaInterface(api_key, selected_model)
        st.rerun()

# Main content area
st.header("Ask a Question")

if not st.session_state.documents:
    st.warning("Please upload at least one document to ask questions.")
elif not st.session_state.huggingface_api_key:
    st.warning("Please enter your Hugging Face API key to ask questions.")
else:
    # Question input
    question = st.text_input("Enter your question:")
    
    # Submit button
    if st.button("Submit", disabled=not question):
        st.session_state.answer = generate_answer(question)
        
    # Display answer
    if st.session_state.answer:
        st.subheader("Answer")
        
        if st.session_state.answer["success"]:
            st.markdown(st.session_state.answer["answer"])
            
            if st.session_state.answer["sources"]:
                st.subheader("Sources")
                for source in st.session_state.answer["sources"]:
                    st.write(f"- {source}")
        else:
            st.error(st.session_state.answer["answer"])

# Footer
st.markdown("---")
st.caption(f"Document Q&A powered by {st.session_state.selected_model}")
