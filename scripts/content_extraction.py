from pdfminer.high_level import extract_text
import json
import os

def extract_text_from_pdf(pdf_path):
    try:
        text_content = {}
        text = extract_text(pdf_path)
        pages = text.split('\x0c')
        
        for page_num, page_text in enumerate(pages):
            text_content[str(page_num)] = page_text.strip()
            print(f"Extracted text from page {page_num}: {page_text[:100]}...")  # Print first 100 characters of the page text

        return text_content
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

if __name__ == "__main__":
    # Set the path to your PDF file directly
    pdf_path = r"C:\Users\Yadav Ji\Documents\GitHub\textbook-QA-system\data\ML_BOOK.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
    else:
        text_content = extract_text_from_pdf(pdf_path)
        
        if text_content is not None:
            # Ensure the 'data' directory exists
            if not os.path.exists('data'):
                os.makedirs('data')
                print(f"Created directory 'data'")
            
            json_file_path = "data/text_content.json"
            with open(json_file_path, "w") as file:
                json.dump(text_content, file, indent=4)
                print(f"Text content extracted and saved to {json_file_path}")

            # Verify if the file was created and has content
            if os.path.exists(json_file_path):
                with open(json_file_path, "r") as file:
                    content = file.read()
                    if content.strip():
                        print(f"File {json_file_path} created successfully and is not empty")
                    else:
                        print(f"File {json_file_path} is empty")
        else:
            print("No text content extracted from the PDF")
