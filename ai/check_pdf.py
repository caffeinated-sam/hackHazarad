import os

def check_pdfs(base_path):
    for disease_folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, disease_folder)
        if os.path.isdir(folder_path):
            # List PDF files inside each disease folder
            pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
            print(f"{disease_folder}: {len(pdf_files)} PDF(s) found")
            
            # Debug: Print the names of the PDF files
            for pdf in pdf_files:
                print(f"  - {pdf}")

# Replace with your actual path
base_path = "D:\\study\\practice\\JeevDead\\data\\medical-papers\\disease"
check_pdfs(base_path)
