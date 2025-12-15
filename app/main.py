from app.llm_engine import LLMEngine
from app.agent import Agent


def main():
    # 1. Start Engine
    print("Starting AI Engine...")
    engine = LLMEngine()

    # 2. Hire Agents
    pm = Agent("Alice (PM)", "You are a concise Product Manager.", engine)
    dev = Agent("Bob (Dev)", "You are a Python Expert. Write code only.", engine)
    qa = Agent(
        "Eve (QA)",
        "You are a meticulous Quality Assurance Engineer. Write the correct code only",
        engine,
    )

    # 3. Run Task
    idea = input("Enter a project idea: ")

    print(f"\nGoal: {idea}")

    # PM breaks it down
    pm_plan = pm.think(f"Create a requirement list for: {idea}")
    print(f"\n--- PM Output ---\n{pm_plan}")

    # Dev writes code
    code = dev.think(f"Here are the requirements:\n{pm_plan}\n\nWrite the code.")
    print(f"\n--- Dev Output ---\n{code}")

    # QA reviews code
    qa_feedback = qa.think(
        f"Here is the code written by the developer:\n{code}\n\nReview it and suggest improvements or solve bugs. Write the new code."
    )
    print(f"\n--- QA Output ---\n{qa_feedback}")


if __name__ == "__main__":
    main()
