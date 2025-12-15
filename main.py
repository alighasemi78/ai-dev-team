import os
from crewai import Agent, Task, Crew, Process, LLM

# 1. SETUP LOCAL LLM
# Note base_url points to the docker service name "ollama"
my_llm = LLM(
    model="ollama/qwen2.5-coder:7b", base_url="http://ollama:11434", verbose=False
)

# 2. DEFINE AGENTS
planner = Agent(
    role="Product Manager",
    goal="Create spec list",
    backstory="Expert PM.",
    verbose=True,
    llm=my_llm,
    allow_delegation=False,
)

developer = Agent(
    role="Python Dev",
    goal="Write code",
    backstory="Python expert.",
    verbose=True,
    llm=my_llm,
    allow_delegation=False,
)

reviewer = Agent(
    role="QA Engineer",
    goal="Fix bugs",
    backstory="Strict reviewer.",
    verbose=True,
    llm=my_llm,
    allow_delegation=False,
)

# 3. TASKS
task1 = Task(
    description="Analyze: '{topic}'. List requirements.",
    expected_output="List",
    agent=planner,
)
task2 = Task(
    description="Write python code for requirements.",
    expected_output="Python Code",
    agent=developer,
)
task3 = Task(
    description="Review and fix code. Return ONLY code.",
    expected_output="Final Code",
    agent=reviewer,
)

# 4. CREW
dev_team = Crew(
    agents=[planner, developer, reviewer],
    tasks=[task1, task2, task3],
    process=Process.sequential,
)

print("## Remote AI Team ##")
topic = input("Enter idea: ")
result = dev_team.kickoff(inputs={"topic": topic})

with open("/app/output/result.py", "w") as f:
    f.write(str(result))
print("Saved to output/result.py")
