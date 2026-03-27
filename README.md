<div align="center">
  <img src="../logo.png" alt="Dexa AI Logo" width="300"/>
  <h1>Dexa AI</h1>
  <p><strong>Autonomous Data Engineering & Machine Learning Agent</strong></p>
</div>

## Overview
**Dexa** is an advanced, terminal-native conversational AI designed to autonomously execute direct tabular data manipulation, statistical analysis, and complex visualization routing. Instead of acting as a standard code-generating assistant, Dexa operates as a live executor—generating bespoke Python frameworks on the fly, evaluating standard actions against `.csv`/`.parquet`/`.xlsx` schemas, and persistently writing structural mutations seamlessly back into your actual source files without intermediate manual coding steps.

### Core Architecture
- **Real-time Syncing:** Actions such as column generation or missing-value imputation write intelligently straight back to the original hard-drive source format.
- **Dynamic Data Visualization:** Dexa evaluates highly complex plotting requests natively, generating aesthetic graphics (e.g. `query_id.png`) uniquely tagged to your active operational context in real-time.
- **Local Context Window Scaling:** Designed to continuously digest iterative commands over prolonged analytical sessions without overflowing the neural inference length.

---

## 🛠 Developer Installation

Ensure your Python environment handles Pandas, Matplotlib, LangGraph, and Typer out-of-the-box.

```bash
git clone https://github.com/your-username/dexa.git
cd dexa
pip install -e .
```

---

## 🚀 Public Usage (Standalone Binary)
For end-users handling large tabular structures without native programming experience, Dexa operates via a completely packaged Windows executable. Note that because Dexa writes Python dynamically, specific dependencies (e.g., `seaborn`, `scikit-learn`) must be available on the host machine if testing extreme custom ML.

1. **Download:** Navigate to the `dist/` folder and launch `Dexa.exe` directly natively.
2. **Access Data:** Place the executable in any accessible location.

### Primary Commands

1. **Authentication Configuration**
Set your LLM credentials centrally to securely power the brain.
```bash
dexa config --groq-key your_groq_api_key_here
```

2. **Load Dataset**
Lock your session onto a local tabular file to synchronize it intelligently.
```bash
dexa load-file C:/path/to/your/custom_dataset.csv
```

3. **Engage the Agent**
Enter the continuous operation framework to begin executing data models textually.
```bash
dexa chat
```

## Example Operations
Inside the chat engine, simply converse aggressively:
- *"Calculate an R-squared multi-variable regression predicting revenue based directly on the other numeric data constraints."*
- *"Fill all NaN elements under my target_column immediately using a generalized mean extrapolation."*
- *"Identify the two most heavily correlated distributions in my matrix and map them together via an elegant Seaborn scatter correlation plot overlay, saving it safely generated via my query ID."*
