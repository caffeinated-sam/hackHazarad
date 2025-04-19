import os
from PyPDF2 import PdfReader

def search_medicine_pdf(medicine_name, folder_path="data/medicine"):
    matches = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    text = page.extract_text()
                    if text and medicine_name.lower() in text.lower():
                        matches.append(f"--- {filename} ---\n{text}")
                        if len(matches) >= 2:
                            break
            except Exception as e:
                print(f"Failed to read {filename}: {e}")
        
        if len(matches) >= 2:
            break

    return "\n\n".join(matches) if matches else "No relevant data found."