# LLaMA Document Q&A

A Streamlit application that allows users to upload documents (text files) and ask questions about them using LLaMA models from Hugging Face.

## Features

- 📄 Upload and process text files
- 🔍 TF-IDF based document chunking and similarity search
- 🤖 Integration with Hugging Face's LLaMA models:
  - LLaMA 4
  - LLaMA 3 (70B)
  - LLaMA 3 (8B)
- 💬 Document context-aware question answering
- 🔄 Easy model switching between different LLaMA versions

## Requirements

- Python 3.7+
- Streamlit
- scikit-learn
- numpy
- requests
- Hugging Face API key with access to LLaMA models

## Installation

1. Clone this repository:
```
git clone <your-repo-url>
cd llama-document-qa
```

2. Install the required packages:
```
pip install streamlit scikit-learn numpy requests
```

3. Run the Streamlit app:
```
streamlit run app.py
```

## Usage

1. Enter your Hugging Face API key in the application
2. Select your preferred LLaMA model version
3. Upload text documents using the file uploader
4. Ask questions in the input field
5. View answers with source attributions

## Project Structure

- `app.py`: Main Streamlit application
- `document_processor.py`: Functions for processing and chunking documents
- `embedding_handler.py`: TF-IDF vectorization and similarity search
- `llama_interface.py`: Interface for Hugging Face API
- `utils.py`: Utility functions for file handling

## Limitations

- Currently only supports text files
- Requires Hugging Face API access to LLaMA models
- Processing large documents may take some time

## License

MIT

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [Hugging Face](https://huggingface.co/)
- [Meta AI](https://ai.meta.com/) for the LLaMA models