import os
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_llm():
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    llm = CTransformers(
        model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        model_type="mistral",
        max_new_tokens=1048,
        temperature=0.3,
        token=hf_token
    )
    return llm

def generate_mcq(document_answer_gen, num_questions=5):
    if not document_answer_gen:
        print("Error: No document content available for question generation.")
        return []

    embeddings = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vector_store = FAISS.from_documents(document_answer_gen, embeddings)

    llm_answer_gen = load_llm()

    answer_generation_chain = RetrievalQA.from_chain_type(
        llm=llm_answer_gen, 
        chain_type="stuff", 
        retriever=vector_store.as_retriever()
    )

    mcq_questions = []
    for i in range(num_questions):
        try:
            mcq_prompt = (
                "Generate a multiple-choice question about the content with 4 options (A, B, C, D) "
                "and provide the correct answer. Format your response as follows:\n"
                "Question: [Your question here]\n"
                "A. [Option A]\n"
                "B. [Option B]\n"
                "C. [Option C]\n"
                "D. [Option D]\n"
                "Correct Answer: [Single letter of correct option (A, B, C, or D)]"
            )
            mcq_response = answer_generation_chain.invoke(mcq_prompt)
            
            # Debug: Print raw response
            print(f"Raw response for question {i+1}:")
            print(mcq_response)
            print("---")

            # Parse the MCQ response
            if isinstance(mcq_response, dict) and 'result' in mcq_response:
                response_text = mcq_response['result']
            else:
                response_text = mcq_response

            # Split the response into lines
            lines = response_text.strip().split('\n')

            # Extract question, options, and correct answer
            question = ""
            options = []
            correct_answer = ""

            for line in lines:
                if line.startswith("Question:"):
                    question = line.replace("Question:", "").strip()
                elif line.startswith(("A.", "B.", "C.", "D.")):
                    options.append(line.strip())
                elif line.startswith("Correct Answer:"):
                    correct_answer = line.replace("Correct Answer:", "").strip()

            # Validate the extracted information
            if question and len(options) == 4 and correct_answer in ['A', 'B', 'C', 'D']:
                mcq_questions.append({
                    "question": question,
                    "options": options,
                    "correct_answer": correct_answer  # This is now just the letter (A, B, C, or D)
                })
            else:
                print(f"Error: Invalid response format for question {i+1}")

        except Exception as e:
            print(f"Error generating question {i+1}: {str(e)}")

    return mcq_questions

if __name__ == "__main__":
    # This part will be handled by the main script
    pass