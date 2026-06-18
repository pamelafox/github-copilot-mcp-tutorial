"""MCP Knowledge Quiz - Test your knowledge of the Model Context Protocol!"""

import random

DEFAULT_QUESTIONS = [
    {
        "question": "What does MCP stand for?",
        "options": {
            "A": "Model Context Protocol",
            "B": "Machine Control Program",
            "C": "Multi-Channel Pipeline",
            "D": "Model Compute Platform",
        },
        "answer": "A",
    },
    {
        "question": "Which transport does MCP use for local servers?",
        "options": {
            "A": "HTTP",
            "B": "WebSocket",
            "C": "stdio",
            "D": "gRPC",
        },
        "answer": "C",
    },
    {
        "question": "What are the three main primitives an MCP server can expose?",
        "options": {
            "A": "Tools, Resources, and Prompts",
            "B": "Functions, Variables, and Templates",
            "C": "Endpoints, Models, and Schemas",
            "D": "Actions, Data, and Views",
        },
        "answer": "A",
    },
    {
        "question": "Which Python framework is commonly used to build MCP servers?",
        "options": {
            "A": "Flask",
            "B": "FastMCP",
            "C": "Django",
            "D": "Streamlit",
        },
        "answer": "B",
    },
    {
        "question": "What analogy is often used to describe MCP?",
        "options": {
            "A": "The Rosetta Stone of AI",
            "B": "USB-C for AI",
            "C": "The Swiss Army Knife of ML",
            "D": "WiFi for agents",
        },
        "answer": "B",
    },
]


class Quiz:
    """An interactive multiple-choice quiz."""

    def __init__(self, questions: list[dict], shuffle: bool = True):
        self.questions = list(questions)
        self.score = 0
        if shuffle:
            random.shuffle(self.questions)

    def display_question(self, index: int, question: dict):
        print(f"Question {index + 1} of {len(self.questions)}")
        print(question["question"])
        print()
        for letter, text in question["options"].items():
            print(f"  {letter}) {text}")
        print()

    def get_user_answer(self, question: dict) -> str:
        valid_options = set(question["options"].keys())
        while True:
            user_input = input("Your answer: ").strip().upper()
            if user_input in valid_options:
                return user_input
            print(f"Please enter one of: {', '.join(sorted(valid_options))}")

    def evaluate_answer(self, user_answer: str, correct_answer: str) -> bool:
        if user_answer == correct_answer:
            print("✅ Correct!\n")
            self.score += 1
            return True
        else:
            print(f"❌ Wrong! The answer was: {correct_answer}\n")
            return False

    def display_results(self):
        total = len(self.questions)
        pct = self.score / total * 100
        print("=" * 50)
        print(f"  Quiz complete! Your score: {self.score}/{total}")
        print(f"  Percentage: {pct:.0f}%")
        if self.score == total:
            print("  🎉 Perfect score!")
        elif pct >= 60:
            print("  👍 Good job!")
        else:
            print("  📚 Keep learning!")
        print("=" * 50)

    def run(self):
        print("=" * 50)
        print("  Welcome to the MCP Knowledge Quiz!")
        print("=" * 50)
        print()

        for i, q in enumerate(self.questions):
            self.display_question(i, q)
            user_answer = self.get_user_answer(q)
            self.evaluate_answer(user_answer, q["answer"])

        self.display_results()


def play_again() -> bool:
    response = input("Play again? (yes/no): ").strip().lower()
    return response in ("yes", "y")


if __name__ == "__main__":
    while True:
        quiz = Quiz(DEFAULT_QUESTIONS)
        quiz.run()
        if not play_again():
            print("Thanks for playing!")
            break
