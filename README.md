# Local LLM with Ollama — Learning Project

A personal learning project documenting my journey of running, customizing, and versioning large language models locally using [Ollama](https://ollama.com).

---

## Overview

This project captures my hands-on experience working with local AI models — from pulling models via the CLI to creating a fully customized model with its own identity and version tag.

---

## What I Learned

### 1. Pulling Models from Ollama
- Used the Ollama CLI to pull pre-built models from the Ollama model registry
- Understood how models are stored and managed locally

```bash
ollama pull llama3.2:3b
```

---

### 2. Running Models via CLI
- Started and interacted with models directly in the terminal
- Learned how to pass prompts and interpret responses from the command line

```bash
ollama run llama3.2:3b
```

---

### 3. Creating a Custom Model
- Used **VS Code** as my IDE to write and manage the model definition
- Defined a custom AI assistant named **James** with a tuned system prompt and temperature
- Built and registered the custom model locally

```bash
ollama create james:latest -f Modelfile
ollama run james:latest
```

---

### 4. Understanding Ollama Model Versioning
- Understood how model tags work in practice by creating and managing `james:latest`

```bash
ollama create james:v1 -f Modelfile
```

---

### 5. Inspecting Models with Ollama Tools
- Used built-in Ollama commands to inspect model metadata and configuration

```bash
/show info        # Display model details (parameters, system prompt, etc.)
ollama list       # List all locally available models
ollama show james:latest  # Show full model specification
```

---

## Tools & Environment

| Tool | Purpose |
|------|---------|
| [Ollama](https://ollama.com) | Local LLM runtime |
| VS Code | IDE for writing the model definition |
| Terminal / CLI | Model interaction and management |
| llama3.2:3b | Base model used for customization |

---

## Project Structure

```
.
├── Modelfile        # Custom model definition for James
└── README.md        # This file
```

---

## Key Takeaways

- Local models give you **full control** over model behavior without API costs
- **Versioning** with tags makes it easy to iterate and roll back model configurations
- CLI tools like `/show info` are essential for debugging and understanding model state
