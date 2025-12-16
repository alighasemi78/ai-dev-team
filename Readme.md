## 🤖 AI Dev Team: From Idea to Code

This repository contains the "AI Dev Team" project, a demonstration of using the **CrewAI** framework to coordinate multiple specialized Language Model Agents to tackle complex development tasks.

The original project was migrated to a raw Hugging Face/PyTorch setup to eliminate dependency issues, but this README documents the successful CrewAI implementation.

---

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine using Docker Compose. This setup relies on a local [Ollama](https://ollama.com/) instance to run the model, ensuring the process is fully self-contained and free.

### Prerequisites

You need the following installed on your system:

-   **Docker**
-   **Docker Compose**
-   **Ollama** (Running locally or configured via the `docker-compose.yml` to run in a container).

### Installation and Setup

1. **Clone the repository:**

```bash
git clone https://github.com/alighasemi78/ai-dev-team.git
cd ai-dev-team
git checkout crewai
```

2. **Ensure Ollama is running:**
   For this project to work, the `qwen2.5-coder:7b` model must be available at `http://ollama:11434`.

    If you are running Ollama in a separate container, ensure its service name matches what is defined in `docker-compose.yml`. If you run Ollama natively on your host machine, you may need to adjust the `OPENAI_API_BASE` environment variable to `http://host.docker.internal:11434/v1` in `docker-compose.yml`.

3. **Prepare the Environment:**
   Ensure your `requirements.txt` includes the necessary packages to avoid the import errors that often plague LiteLLM/CrewAI setups:

```text
crewai
crewai-tools
litellm
fastapi
uvicorn
apscheduler
email-validator
```

4. **Build and Run the Service:**
   Use Docker Compose to build the application image and run your task.

```bash
# 1. Build the service image
docker compose up --build -d

# 2. Execute the crew, removing the container upon completion
docker compose run --rm dev-team
```

---

## 🧠 Crew Design and Architecture

This project utilizes three core agents, each assigned a specialized role and a dedicated tool to maximize efficiency and minimize hallucination.

### The Crew

| Agent Name                 | Role / Persona                                           | Goal                                                                                                                 | Tool (if applicable)          |
| -------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **Product Manager**        | Defines high-level requirements and acceptance criteria. | Break down complex user ideas into concrete, actionable tasks for the developer.                                     | `None` (Focus is on planning) |
| **Tech Lead**              | Focuses on file structure and class design.              | Take the PM's requirements and generate the final, executable Python code, using the file system to save the result. | `CodeExecutionTool`           |
| **Quality Assurance (QA)** | Reviews code and verifies output against requirements.   | Execute the generated code and report on whether the output successfully meets the original user requirements.       | `CodeExecutionTool`           |

### The Workflow

The agents are orchestrated using a **Sequential Process**:

1. **PM ➡️ Tech Lead:** The Product Manager receives the **User Idea** and outputs a detailed **Feature List**. This list is the input for the Tech Lead.
2. **Tech Lead ➡️ QA:** The Tech Lead writes the complete Python **Code** and saves it to a file. The file path and requirements are passed to the QA Agent.
3. **QA ➡️ Output:** The QA Agent executes the code and provides a final **Verification Report** detailing success or failure.

---

## ⚙️ Configuration Details

The entire environment is configured via the `docker-compose.yml` file, which routes all LLM API calls to the local Ollama service.

### Environment Variables

| Variable                   | Value                    | Purpose                                                                            |
| -------------------------- | ------------------------ | ---------------------------------------------------------------------------------- |
| `OPENAI_API_BASE`          | `http://ollama:11434/v1` | Redirects CrewAI/LiteLLM calls to the Ollama server endpoint.                      |
| `OPENAI_API_KEY`           | `NA`                     | Required by the LiteLLM library, but the value is irrelevant for Ollama.           |
| `OPENAI_MODEL_NAME`        | `qwen2.5-coder:7b`       | Specifies the LLM model to be used by the Crew.                                    |
| `LITELLM_TELEMETRY`        | `False`                  | Crucial for suppressing background usage logging and associated dependency errors. |
| `CREWAI_TELEMETRY_OPT_OUT` | `true`                   | Additional flag to ensure CrewAI's own logging is disabled.                        |

### Note on `litellm` Dependencies

The repeated dependency errors (`fastapi-sso`) encountered during development highlight a common issue with highly-coupled Python frameworks. These errors don't have any effect on the performance of the program as the output is stored in the right place at the end of the run!
