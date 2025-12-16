## 🤖 AI Dev Team: From Scratch with Hugging Face & PyTorch

This repository represents the **production-ready** version of the AI Dev Team project. It moves away from high-level, opinionated frameworks (like CrewAI/LiteLLM) to directly leverage the industry-standard **Hugging Face `transformers`** library and **PyTorch**.

This approach provides **maximum control**, eliminates dependency hell, and guarantees the LLM operates exactly as configured, with full GPU utilization via quantization.

---

## ✨ Key Features

-   **Bare-Metal Control:** No intermediate APIs or proxy layers (no LiteLLM, no CrewAI).

-   **Direct GPU Access:** Utilizes **PyTorch** and **Bitsandbytes (4-bit quantization)** to run large models (e.g., Qwen 7B) efficiently on consumer GPUs.
-   **Custom Agent Workflow:** Implements a clean, custom `Agent` class for explicit state management and manual multi-agent orchestration.
-   **Dockerized CUDA:** Uses an official NVIDIA CUDA base image for guaranteed environment stability.

---

## 🚀 Getting Started (GPU Required)

This setup is designed for systems with an **NVIDIA GPU** and the **NVIDIA Container Toolkit** installed, as it requires direct GPU access from within the Docker container.

### Prerequisites

-   **Docker** and **Docker Compose**
-   **NVIDIA GPU**
-   **NVIDIA Container Toolkit** (Allows Docker to see your GPU)

### Installation and Setup

1. **Project Structure:** Ensure your project follows the structure defined in the instructions:

```text
ai-from-scratch/
├── app/
│   ├── main.py       # Orchestration
│   ├── agent.py      # Agent Class/Logic
│   └── llm_engine.py # Model/Hardware Handler
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

2. **Define Dependencies (`requirements.txt`):**

```text
torch
transformers
accelerate
bitsandbytes
scipy
sentencepiece
protobuf
```

3. **Build the Container:** This process pulls the NVIDIA base image and installs all dependencies, ensuring a stable CUDA environment.

```bash
docker compose up --build -d
```

4. **Run the Engine:** The first time this runs, it will download the **Qwen/Qwen2.5-Coder-7B-Instruct** model weights (approx 4-5GB) to the local `./hf_cache` folder.

```bash
docker compose run --rm llm-engine
```

---

## 🛠️ Architecture and Model Handling

### 1. `llm_engine.py` (The Engine)

This file handles the hardware and memory management, a critical step that was previously managed by LiteLLM.

-   **Model Loading:** The `Qwen/Qwen2.5-Coder-7B-Instruct` model is loaded once at startup.
-   **Quantization:** It configures `BitsAndBytesConfig(load_in_4bit=True)` to compress the model weights, dramatically reducing VRAM usage and making it feasible to run the 7B model on consumer GPUs.
-   **Inference:** It manages tokenization, moving tensors to the GPU, and decoding the final response text.

### 2. `agent.py` (The Brain)

This minimal class replaces the complexity of CrewAI's agent implementation.

-   **State Management:** The `history` list explicitly stores past turns (`user` and `assistant`), giving the agent memory.
-   **Role Enforcement:** Each call prepends the agent's unique `system_prompt` to the request, maintaining the persona (e.g., "Python Architect") throughout the conversation.

### 3. `main.py` (The Orchestrator)

This file defines the manual, sequential workflow, replacing the declarative `SequentialProcess` of CrewAI.

1. Initializes a single, shared `LLMEngine`.
2. Instantiates `Agent` objects (PM, Dev, QA) using the shared engine.
3. Manually passes the output from the **Product Manager**'s `think()` method as the input for the **Tech Lead**'s next `think()` method and then the generated code to **Quality Assurance Enginner** for final review.

---

## 🐳 Docker Configuration (`docker-compose.yml`)

The `docker-compose.yml` file is configured for optimal GPU usage and caching:

```yaml
services:
    llm-engine:
        # ... build details ...
        runtime: nvidia # Enables GPU access via NVIDIA Container Toolkit
        volumes:
            # CRITICAL: Persists the 5GB model download on your host machine
            - ./hf_cache:/root/.cache/huggingface
            # Maps local code edits directly to the container
            - ./app:/app/app
        deploy:
            resources:
                reservations:
                    devices:
                        - driver: nvidia
                          count: 1
                          capabilities: [gpu] # Ensures the container reserves a GPU
```
