import os
import zipfile
import shutil

# Create a temporary directory
temp_dir = "streamlit_llama_qa"
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
os.makedirs(temp_dir)

# Copy necessary files
files_to_copy = [
    "app.py",
    "document_processor.py",
    "embedding_handler.py",
    "llama_interface.py",
    "utils.py",
    "README.md"
]

for file in files_to_copy:
    shutil.copy(file, os.path.join(temp_dir, file))

# Create .streamlit directory in the temp folder
streamlit_dir = os.path.join(temp_dir, ".streamlit")
os.makedirs(streamlit_dir, exist_ok=True)
shutil.copy(".streamlit/config.toml", os.path.join(streamlit_dir, "config.toml"))

# Create requirements.txt
requirements = [
    "streamlit==1.44.0",
    "scikit-learn==1.3.0",
    "numpy==1.24.4",
    "requests==2.31.0"
]

with open(os.path.join(temp_dir, "requirements.txt"), "w") as f:
    f.write("\n".join(requirements))

# Create ZIP file
zip_path = "streamlit_llama_qa.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    # Add all files from the temp directory
    for root, _, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, temp_dir)
            zipf.write(file_path, os.path.join(os.path.basename(temp_dir), relative_path))

print(f"ZIP file created successfully at: {os.path.abspath(zip_path)}")

# Print the contents of the ZIP file
print("\nContents of the ZIP file:")
with zipfile.ZipFile(zip_path, "r") as zipf:
    for file in zipf.namelist():
        print(f"  {file}")