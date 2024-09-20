import csv
import os
from datetime import datetime
import random

def save_questions_to_csv(subject, questions):
    filename = f"{subject.lower()}_quiz.csv"
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Question', 'Option A', 'Option B', 'Option C', 'Option D', 'Correct Option'])
        
        for q in questions:
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                q['question'],
                q['options'][0][3:], 
                q['options'][1][3:],
                q['options'][2][3:], 
                q['options'][3][3:], 
                q['correct_answer'][0] 
            ])

def get_questions_from_csv(subject, num_questions=5):
    filename = f"{subject.lower()}_quiz.csv"
    if not os.path.isfile(filename):
        return []
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        questions = list(reader)
    
    random.shuffle(questions)
    
    selected_questions = []
    seen_questions = set()
    for q in questions:
        if q[1] not in seen_questions:
            selected_questions.append(q)
            seen_questions.add(q[1])
            if len(selected_questions) == num_questions:
                break
    
    formatted_questions = []
    for q in selected_questions:
        formatted_questions.append({
            'question': q[1],
            'options': [f"A. {q[2]}", f"B. {q[3]}", f"C. {q[4]}", f"D. {q[5]}"],
            'correct_answer': q[6]
        })
    
    return formatted_questions

def run_quiz_from_csv(subject):
    questions = get_questions_from_csv(subject)
    if not questions:
        print(f"No questions available for {subject}.")
        return
    
    if len(questions) < 5:
        print(f"Warning: Only {len(questions)} questions available for the quiz.")
    
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for option in q['options']:
            print(option)
        
        user_answer = input("Your answer (A, B, C, or D): ").upper()
        correct_answer = q['correct_answer']
        
        if user_answer == correct_answer:
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect. The correct answer was {correct_answer}.")
    
    print(f"\nQuiz completed. Your score: {score} out of {len(questions)}")

if __name__ == "__main__":
    pass