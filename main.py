import os
from pdf_processor import process_pdf, file_processing
from quiz_script import generate_mcq
from csv_operations import save_questions_to_csv, run_quiz_from_csv

def check_pdf_availability(subject):
    pdf_filename = f"pdfs/{subject.lower()}.pdf"
    return os.path.isfile(pdf_filename)

def admin_flow():
    pdf_file = input("Enter the path to your PDF file: ")
    processed_file = process_pdf(pdf_file)
    print(f"PDF processed and saved as: {processed_file}")

def user_flow():
    subject = input("Enter the subject for the quiz: ")
    if check_pdf_availability(subject):
        print(f"Generating new questions for {subject}...")
        pdf_path = f"pdfs/{subject.lower()}.pdf"
        document_ques_gen, document_answer_gen = file_processing(pdf_path)
        
        max_attempts = 1
        for attempt in range(max_attempts):
            mcq_questions = generate_mcq(document_answer_gen)
            
            if mcq_questions:
                break
            # else:
            #     print(f"Attempt {attempt + 1} failed to generate questions. Retrying...")
        
        if mcq_questions:
            # Save newly generated questions to CSV
            save_questions_to_csv(subject, mcq_questions)
            print(f"New questions for {subject} have been generated.")
            
            # Run the quiz with the newly generated questions
        run_quiz_from_csv(subject)
        # else:
        #     print(f"Failed to generate questions for {subject} after {max_attempts} attempts.")
    else:
        print(f"Sorry, the PDF for {subject} is not available.")

def main():
    while True:
        user_type = input("Are you a user or admin? (user/admin): ").lower()
        
        if user_type == "admin":
            admin_flow()
            break
        elif user_type == "user":
            user_flow()
            break
        else:
            print("Invalid input. Please enter 'user' or 'admin'.")

if __name__ == "__main__":
    main()