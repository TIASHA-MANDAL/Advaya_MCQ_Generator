import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def process_pdf(pdf_path):
    if not os.path.exists('pdfs'):
        os.makedirs('pdfs')

    original_filename = os.path.basename(pdf_path)

    new_filename = input(f"Enter a new name for {original_filename} (without .pdf extension): ")
    new_filename = f"{new_filename}.pdf"

    new_path = os.path.join('pdfs', new_filename)
    shutil.copy2(pdf_path, new_path)

    print(f"File copied and renamed to: {new_path}")

    return new_path

def file_processing(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()

    question_gen = ''
    for page in data:
        question_gen += page.page_content

    splitter_ques_gen = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks_ques_gen = splitter_ques_gen.split_text(question_gen)
    document_ques_gen = [Document(page_content=t) for t in chunks_ques_gen]

    splitter_ans_gen = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30
    )

    document_answer_gen = splitter_ans_gen.split_documents(document_ques_gen)
    return document_ques_gen, document_answer_gen

if __name__ == "__main__":
    pdf_file = input("Enter the path to your PDF file: ")
    processed_file = process_pdf(pdf_file)
    print(f"PDF processed: {processed_file}")
