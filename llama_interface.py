import os
import requests
from typing import Optional, Dict, Any, List
import logging
import streamlit as st
import json

class LlamaInterface:
    """
    Interface for LLaMA models from Hugging Face.
    """
    
    # Available models to choose from
    AVAILABLE_MODELS = {
        "Meta-Llama-4": "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-4",
        "Meta-Llama-3-70B-Instruct": "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct",
        "Meta-Llama-3-8B-Instruct": "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    }
    
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initialize the LLaMA interface with a Hugging Face API key.
        
        Args:
            api_key: Optional API key (will use env var if not provided)
            model_name: Optional model name to use (will default to LLaMA 4)
        """
        # Check for API key in session state first
        if "huggingface_api_key" in st.session_state:
            self.api_key = st.session_state.huggingface_api_key
        else:
            self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
            
        # Set model from session_state or parameter
        if model_name and model_name in self.AVAILABLE_MODELS:
            self.model_name = model_name
        elif "selected_model" in st.session_state and st.session_state.selected_model in self.AVAILABLE_MODELS:
            self.model_name = st.session_state.selected_model
        else:
            self.model_name = "Meta-Llama-4"  # Default to LLaMA 4
        
        # Set model endpoint
        self.model_endpoint = self.AVAILABLE_MODELS[self.model_name]
        
        if not self.api_key:
            logging.warning("No Hugging Face API key provided. Functionality will be limited.")
    
    def generate_response(self, 
                          question: str, 
                          context: str = "", 
                          temperature: float = 0.7, 
                          max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Generate a response from LLaMA 4 based on question and context.
        
        Args:
            question: The user's question
            context: Optional context from documents
            temperature: Controls randomness (0-1)
            max_tokens: Maximum output length
            
        Returns:
            Dictionary with response information
        """
        if not self.api_key:
            return {
                "answer": "Error: No Hugging Face API key provided.",
                "sources": [],
                "success": False
            }
            
        try:
            # Prepare prompt as messages for LLaMA 4
            if context:
                messages = [
                    {
                        "role": "system",
                        "content": "You are an AI assistant that answers questions based on the provided context. If the context doesn't contain relevant information to answer the question, admit that you don't know. Always cite your sources by referring to the file name when providing information."
                    },
                    {
                        "role": "user",
                        "content": f"Context information is below:\n\n{context}\n\nQuestion: {question}\n\nAnswer the question based on the context provided."
                    }
                ]
            else:
                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
                
            # Convert to JSON format expected by the API
            prompt = json.dumps(messages)
            
            # Call Hugging Face API for inference
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "temperature": temperature,
                    "max_new_tokens": max_tokens,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.model_endpoint,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    answer = result[0].get("generated_text", "No answer generated.")
                else:
                    answer = str(result)
                
                # Extract sources from context if possible
                sources = []
                if context:
                    # Simple extraction of file names from context
                    context_parts = context.split("Context ")
                    for part in context_parts:
                        if "(from " in part:
                            source = part.split("(from ")[1].split(")")[0]
                            if source not in sources:
                                sources.append(source)
                
                return {
                    "answer": answer,
                    "sources": sources,
                    "success": True
                }
            else:
                error_message = f"Error: API returned status code {response.status_code}."
                try:
                    error_details = response.json()
                    error_message += f" Details: {json.dumps(error_details)}"
                except:
                    error_message += f" Response: {response.text}"
                
                return {
                    "answer": error_message,
                    "sources": [],
                    "success": False
                }
                
        except Exception as e:
            return {
                "answer": f"Error generating response: {str(e)}",
                "sources": [],
                "success": False
            }
