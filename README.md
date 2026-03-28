<div align="center">
  <img src="./logo.png" alt="Dexa Logo" width="300"/>
  <h1>Dexa</h1>
  <p><strong>Terminal-First Agentic AI Copilot for Machine Learning Engineers</strong></p>
  <p>
    <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python"/>
    <img alt="LangGraph" src="https://img.shields.io/badge/Orchestration-LangGraph-green?style=flat-square"/>
    <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square"/>
  </p>
</div>

---

## What is Dexa?

**Dexa** is NOT a chatbot. NOT a simple code generator. NOT just another AutoML wrapper.

Dexa is a **terminal-first, agentic AI copilot** built specifically for Machine Learning Engineers who do not want to manually handle repetitive data science and data engineering work.

Think of Dexa as an **intelligent ML teammate** that can think, plan, execute, evaluate, and improve its own decisions — step by step.

> **Query → Understand → Plan → Execute → Reflect → Adapt → Respond**

---

## Core Capabilities

Dexa helps you:

- 📊 **Analyze datasets** — summaries, statistics, distributions
- 🔗 **Understand feature relationships** — correlations, dependencies
- 🔍 **Detect data quality issues** — missing values, skewness, outliers, imbalance, leakage
- 🔧 **Suggest preprocessing steps** — imputation, encoding, scaling strategies
- 🤖 **Recommend models** — matched to your task and data profile
- 📈 **Suggest evaluation metrics** — appropriate for your problem type
- ⚙️ **Generate ML pipelines** — lightweight, actionable, end-to-end
- 🩺 **Diagnose ML problems** — low accuracy, overfitting, data leakage, bad feature selection
- 🪜 **Execute step-by-step** — instead of giving one-shot answers

---

## Design Philosophy

Dexa is built around one core idea: **reduce manual effort before model training**.

Every action Dexa takes follows these principles:

- ✅ Think before acting
- ✅ Break tasks into smaller executable steps
- ✅ Execute only one step at a time
- ✅ Evaluate the result of each step
- ✅ Decide whether to continue, replan, or stop
- ✅ Prefer deterministic tools over hallucinated code
- ✅ Give actionable ML insights instead of generic summaries

---

## Architecture

Dexa is built on a **modular multi-agent architecture** orchestrated by **LangGraph**.

### Agents

| Agent | Role |
|---|---|
| `IntentAgent` | Understands what the user wants |
| `GoalAgent` | Handles goal-oriented tasks (prediction, regression, forecasting, etc.) |
| `PlannerAgent` | Breaks tasks into small, executable steps |
| `ExecutionAgent` | Chooses how to perform each step (tool or code) |
| `ReflectionAgent` | Evaluates whether the step succeeded |
| `ReasoningAgent` | Synthesizes findings and recommendations |
| `ResponseAgent` | Formats the final response |
| `ProfilerAgent` | Understands dataset characteristics |
| `VisualizationAgent` | Decides whether and what to visualize |

### LangGraph Flow

Dexa is controlled by a **LangGraph state machine**, not a linear orchestrator.

```
Intent → Goal → Planner → Step → Execution → Reflection → Step Control
```

After **Step Control**, Dexa dynamically decides what to do next based on `ReflectionAgent` output:

```json
{
  "decision": "continue | replan | stop",
  "reason": "...",
  "issues": [],
  "confidence": 0.0
}
```

Dexa is **adaptive** — it can change strategy mid-execution without user intervention.

---

## Execution System

### Tool-First Approach

Dexa always **prefers deterministic tools** over LLM-generated code.

`ExecutionAgent` outputs one of two formats:

**Tool usage (preferred):**
```json
{
  "type": "tool",
  "tool_name": "describe_data",
  "args": {}
}
```

**Fallback code generation:**
```json
{
  "type": "code",
  "code": "df['income_per_age'] = df['income'] / df['age']"
}
```

Code is only generated when no existing tool fits the task.

### Built-in Tools

Dexa ships with deterministic tools for common ML tasks:

- Dataset summary & profiling
- Missing value detection
- Feature statistics
- Correlation heatmaps
- Histogram plotting
- Linear model training
- Data quality checks
- Outlier & skewness detection

### Code Execution

For complex or unsupported tasks, `ExecutionAgent` can generate and safely execute Python code using:

- `pandas` · `numpy` · `matplotlib` · `seaborn`
- `sklearn` · `scipy` · `statsmodels`

The **Executor** runs this code in a controlled environment, capturing stdout, return values, and errors — and feeding results back into Dexa's state.

---

## Visualization

Visualization is **lightweight and tool-based**.

`VisualizationAgent` only decides:
- Whether visualization is useful
- Which chart type is appropriate
- Which columns to visualize

```json
{
  "should_visualize": true,
  "plot_type": "histogram",
  "column": "price"
}
```

`ExecutionAgent` then converts this into a tool call or plotting code. Supported chart types include: histograms, correlation heatmaps, scatter plots, box plots, and feature distributions.

---

## Installation

Choose the installation method that works best for you.

---

### Option 1 — pip (Standard)

> Recommended for developers and ML engineers who already have Python 3.10+ installed.

```bash
# Clone the repository
git clone https://github.com/ath34-tech/dexa.git
cd dexa

# Install in editable mode
pip install -e .
```

**Requirements:** Python 3.10+, pip

---

### Option 2 — Standalone Executable (Windows)

> No Python installation required. Download and run immediately.

1. Go to the [**Releases**](https://github.com/ath34-tech/dexa/releases) page
2. Download the latest `Dexa.exe` from the Assets section
3. Place `Dexa.exe` in any folder you prefer (e.g. `C:\Tools\dexa\`)
4. Add that folder to your system `PATH` so you can run `dexa` from any terminal
5. Open a terminal and verify:

```cmd
dexa --help
```

> **Note:** Advanced ML operations (e.g. custom sklearn pipelines, seaborn plots) may require the relevant Python packages to be present on your machine.

---

### Option 3 — uv (Fast Python Toolchain)

> Recommended if you use [uv](https://github.com/astral-sh/uv) as your Python package manager.

```bash
# Install uv if you haven't already
curl -Ls https://astral.sh/uv/install.sh | sh

# Clone and install Dexa
git clone https://github.com/your-username/dexa.git
cd dexa

# Create a virtual environment and install
uv venv
uv pip install -e .

# Activate the environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

> `uv` is significantly faster than pip for dependency resolution and installation.

---

## Configuration

Before running Dexa, configure your credentials. You can set them once with `dexa config` and they will be persisted to a local `.env` file for all future sessions.

```bash
# Set your Groq API key (required)
dexa config --groq-key YOUR_GROQ_API_KEY

# Optionally set a specific Groq model
dexa config --model-name llama-3.1-8b-instant

# Optionally configure Kaggle credentials (for dataset downloads)
dexa config --kaggle-username YOUR_KAGGLE_USERNAME --kaggle-key YOUR_KAGGLE_KEY
```

All values are saved to `.env` at the project root and automatically reloaded on the next run.

---

## CLI Reference

Dexa is **terminal-first**. Every command is designed to feel like a developer tool, not a chat app.

### `dexa config`

Persist credentials and settings to the local `.env` file.

```bash
dexa config [OPTIONS]

Options:
  --groq-key TEXT          Set your Groq API key
  --model-name TEXT        Set the Groq model to use (e.g. llama-3.1-8b-instant)
  --kaggle-username TEXT   Set your Kaggle username
  --kaggle-key TEXT        Set your Kaggle API key
```

---

### `dexa load-file`

Load a local dataset (CSV, Parquet, or Excel) into the session context.

```bash
dexa load-file path/to/dataset.csv
dexa load-file path/to/dataset.parquet
dexa load-file path/to/dataset.xlsx
```

> `dexa load-data` is an alias for the same command.

---

### `dexa load-kaggle`

Download and load a dataset directly from Kaggle.

```bash
dexa load-kaggle username/dataset-name

# Optionally pass credentials inline
dexa load-kaggle username/dataset-name --username YOUR_USERNAME --key YOUR_KAGGLE_KEY
```

Kaggle credentials can also be pre-set via `dexa config`.

---

### `dexa chat`

Start an interactive agentic session. This is the main command for querying Dexa.

```bash
dexa chat

# Optionally override credentials for this session only
dexa chat --api-key YOUR_GROQ_API_KEY
dexa chat --model-name llama-3.1-8b-instant
dexa chat --kaggle-username YOUR_USERNAME --kaggle-key YOUR_KEY
```

Once inside the session, type any natural language question and Dexa will think, plan, execute, reflect, and respond.

Type `exit` or `quit` to end the session.

---

## Usage Tutorial

This tutorial walks you through a real end-to-end Dexa workflow.

---

### Step 1 — Configure Credentials

Run this once. Your settings are saved and reused in every future session.

```bash
dexa config --groq-key YOUR_GROQ_API_KEY
```

To also set a model and Kaggle access:

```bash
dexa config \
  --groq-key YOUR_GROQ_API_KEY \
  --model-name llama-3.1-8b-instant \
  --kaggle-username YOUR_USERNAME \
  --kaggle-key YOUR_KAGGLE_KEY
```

---

### Step 2 — Load Your Dataset

#### From a local file:

```bash
dexa load-file path/to/housing.csv
```

#### From Kaggle:

```bash
dexa load-kaggle ath34-tech/housing-prices-dataset
```

Dexa will confirm the file is loaded and ready for querying.

---

### Step 3 — Start a Chat Session

```bash
dexa chat
```

You'll see the Dexa prompt:

```
Welcome to Dexa AI! Type 'exit' to quit.

>>
```

From here, ask anything about your data in plain English.

---

### Step 4 — Query Dexa

Inside the chat session, Dexa handles everything through natural language. Some example queries:

```
>> What does this dataset look like? Summarize its structure.
>> Are there any missing values? How should I handle them?
>> What features are most correlated with the target column?
>> Is there any risk of data leakage in this dataset?
>> Detect any outliers in the price column.
>> What model would you recommend for a regression task on this data?
>> What preprocessing steps should I apply before training?
>> Show me a correlation heatmap of all numeric features.
>> Why might a model trained on this data be overfitting?
>> Generate a lightweight ML pipeline for predicting house_price.
```

Dexa will **think → plan → execute step-by-step → reflect → adapt**, all without you writing a single line of code.

---

### Full Workflow Example

```bash
# Step 1: Configure once
dexa config --groq-key sk-your-key-here --model-name llama-3.1-8b-instant

# Step 2: Load a local dataset
dexa load-file housing.csv

# Step 3: Enter the chat session
dexa chat
```

```
Welcome to Dexa AI! Type 'exit' to quit.

>> What are the most important features for predicting house_price?

 Thinking...

Dexa AI:
┌─────────────────────────────────────────────────────────────────┐
│ Based on correlation analysis:                                  │
│                                                                 │
│ Top features correlated with house_price:                       │
│  • OverallQual  → 0.79                                          │
│  • GrLivArea    → 0.71  (⚠ skewed, consider log-transform)     │
│  • GarageCars   → 0.64                                          │
│  • TotalBsmtSF  → 0.61                                          │
│                                                                 │
│ Recommendation: Apply log1p to GrLivArea before training.       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Usage Tutorial

This tutorial walks you through a complete Dexa workflow — from loading your data to getting actionable ML insights.

### Step 1 — Set Your API Key

```bash
dexa config --groq-key YOUR_GROQ_API_KEY
```

This only needs to be done once. Dexa stores the key locally for future sessions.

---

### Step 2 — Profile Your Dataset

Get a high-level understanding of your data before doing anything else.

```bash
dexa profile data.csv
```

Dexa will report:
- Row and column counts
- Data types per feature
- Missing value counts and percentages
- Skewness and outlier flags
- Class imbalance warnings (for classification targets)

---

### Step 3 — Analyze the Dataset

Run a deeper analysis to detect quality issues and understand feature relationships.

```bash
dexa analyze data.csv
```

Dexa will:
- Summarize feature distributions
- Detect correlations between columns
- Flag potential data leakage
- Highlight redundant or low-variance features

---

### Step 4 — Diagnose ML Problems

Already have a model but something feels off? Tell Dexa what's wrong.

```bash
dexa diagnose "low accuracy"
dexa diagnose "model is overfitting"
dexa diagnose "features don't seem useful"
dexa diagnose "training and test scores are very different"
```

Dexa will reason through the problem, identify likely causes, and suggest concrete next steps.

---

### Step 5 — Generate an ML Pipeline

Tell Dexa which column you want to predict and it will generate a full pipeline suggestion.

```bash
dexa pipeline --target price
dexa pipeline --target churn
dexa pipeline --target sales_volume
```

Dexa will recommend:
- Preprocessing steps (imputation, encoding, scaling)
- A suitable model for the task type
- Appropriate evaluation metrics
- A lightweight, runnable pipeline structure

---

### Step 6 — Start an Interactive Session

For multi-turn, exploratory analysis, load your file and enter the chat mode.

```bash
dexa load-file path/to/dataset.csv
dexa chat
```

Inside the interactive session, ask Dexa anything:

```
> What features are most correlated with the target column?
> Detect missing values and suggest imputation strategies.
> Why might my model be overfitting?
> Recommend a model for this regression task.
> Plot the distribution of the price column.
> Identify the top 5 most important features.
> Is there any data leakage in this dataset?
> What preprocessing steps should I apply before training?
> Show me a correlation heatmap of all numeric columns.
> Flag any outliers in the age column.
```

Dexa will **think, plan, execute step-by-step, reflect on each result**, and adapt its strategy — all autonomously.

---

### Full Workflow Example

```bash
# 1. Configure once
dexa config --groq-key sk-...

# 2. Profile the raw dataset
dexa profile housing.csv

# 3. Run a full analysis
dexa analyze housing.csv

# 4. Generate a pipeline for your target
dexa pipeline --target house_price

# 5. Jump into interactive mode for deeper exploration
dexa load-file housing.csv
dexa chat
```

```
[Dexa] Loaded housing.csv — 1,460 rows × 81 columns
[Dexa] Thinking...

> What are the most important features for predicting house_price?

[Dexa] Planning → Profiling features → Running correlation analysis → Evaluating skewness
[Dexa] Top correlated features: OverallQual (0.79), GrLivArea (0.71), GarageCars (0.64)
[Dexa] Recommendation: Consider log-transforming GrLivArea (skew: 1.27)
```

---

## Future Vision

- 🧠 Richer memory and session continuity
- 🔧 Expanded deterministic toolset
- 🤖 AutoML-lite pipelines
- 📊 Experiment tracking integration
- 🔎 Advanced visualization reasoning
- 🖥️ VS Code extension
- 🩺 Enhanced diagnosis mode
- 🔀 More advanced LangGraph routing

---

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph |
| CLI | Typer |
| Data | pandas, numpy |
| ML | scikit-learn, scipy, statsmodels |
| Visualization | matplotlib, seaborn |
| LLM Backend | Groq (configurable) |

---

<div align="center">
  <sub>Built for ML Engineers who want to move faster — without cutting corners.</sub>
</div>
