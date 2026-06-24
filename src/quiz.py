"""MCP Knowledge Quiz - Test your knowledge of the Model Context Protocol!"""

QUESTIONS = [
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


def run_quiz():
    print("=" * 50)
    print("  Welcome to the MCP Knowledge Quiz!")
    print("=" * 50)
    print()

    score = 0

    for i, q in enumerate(QUESTIONS):
        print(f"Question {i + 1} of {len(QUESTIONS)}")
        print(q["question"])
        print()
        for letter, text in q["options"].items():
            print(f"  {letter}) {text}")
        print()

        user_answer = input("Your answer: ")

        if user_answer == q["answer"]:
            print("✅ Correct!\n")
            score += 1
        else:
            print("❌ Wrong!\n")

    print("=" * 50)
    print(f"  Quiz complete! Your score: {score}/{len(QUESTIONS)}")
    pct = score / len(QUESTIONS) * 100
    print(f"  Percentage: {pct:.0f}%")
    print("=" * 50)


if __name__ == "__main__":
    run_quiz()
