import os

# Folder where your research papers are stored
BASE_PATH = "./data/medical-papers"

# Check how many PDFs are in each disease folder
def check_pdfs(base_path):
    for disease_folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, disease_folder)
        if os.path.isdir(folder_path):
            pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
            print(f"{disease_folder}: {len(pdf_files)} PDF(s) found")

check_pdfs(BASE_PATH)
