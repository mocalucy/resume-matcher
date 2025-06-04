import string
import json
import PyPDF2

def read_pdf(file_path):
    output = None
    try:
        pdf_obj = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_obj)
        page_obj = pdf_reader.pages[0]
        output = page_obj.extract_text()
        pdf_obj.close()
    except Exception as e:
        print(f"Error reading file '{file_path}': {str(e)}")
    return output

