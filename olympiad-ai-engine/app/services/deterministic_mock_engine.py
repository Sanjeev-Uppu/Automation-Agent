import random

def generate_mock_exam(context, chapter_name):

    sample_questions = [
        {
            "id": 1,
            "question": "Which of the following is a mammal?",
            "options": ["Frog", "Whale", "Snake", "Crocodile"],
            "correct_answer": "Whale"
        },
        {
            "id": 2,
            "question": "Which animal lays eggs?",
            "options": ["Cow", "Goat", "Hen", "Dog"],
            "correct_answer": "Hen"
        },
        {
            "id": 3,
            "question": "Which animal undergoes metamorphosis?",
            "options": ["Frog", "Cow", "Dog", "Cat"],
            "correct_answer": "Frog"
        },
        {
            "id": 4,
            "question": "Which is an aquatic animal?",
            "options": ["Camel", "Whale", "Tiger", "Monkey"],
            "correct_answer": "Whale"
        },
        {
            "id": 5,
            "question": "Which animal gives birth to young ones?",
            "options": ["Snake", "Hen", "Cow", "Frog"],
            "correct_answer": "Cow"
        }
    ]

    random.shuffle(sample_questions)

    return {
        "intent": "mock_exam",
        "chapter": chapter_name,
        "duration_minutes": 15,
        "questions": sample_questions[:5]
    }
