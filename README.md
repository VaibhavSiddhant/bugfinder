# BugFinder — Real-Time C++ Bug Detector for LeetCode

Real-time C++ code analysis tool that detects bugs, vulnerabilities and syntax errors as you type on LeetCode. Combines static analysis with a fine-tuned CodeBERT model trained on real CVE data.

---

## Demo

The Chrome extension analyzes your C++ code every 3 seconds and shows a live panel with warnings directly on LeetCode.

---

## Architecture
`
LeetCode Editor (C++ code)
        |
Chrome Extension (content.js)
        |
FastAPI Backend (port 8000)
        |
   +----+----+
   |         |
Static     CodeBERT
Analyzer   (Fine-tuned)
   |         |
   +----+----+
        |
  JSON Response
        |
Live Panel on LeetCode
`

---

## Features

### Static Analyzer (Rule-based, Instant)
| Feature | Example |
|---|---|
| O(n^2) complexity detection | Nested loops warning before submission |
| Infinite loop risk | while(true) or while(1) |
| Assignment in condition | if(x=5) instead of if(x==5) |
| Array bounds risk | Array access without size check |
| Pointer null dereference | Pointer usage without null check |
| Mismatched braces | Missing or extra {} |
| Mismatched parentheses | Missing or extra () |
| Missing semicolons | Statement without ; |
| Colon instead of semicolon | int x = 5: instead of ; |
| Return in void function | void func returning value |
| Missing return statement | Non-void function without return |
| 30+ C++ typo patterns | whil( fro( intt voud esle etc |

### ML Model (CodeBERT Fine-tuned)
- Fine-tuned microsoft/codebert-base on BigVul dataset
- 3200 real C/C++ CVEs from GitHub
- Detects buffer overflows, memory corruption, unsafe C++ patterns
- F1 Score: 0.93 | Accuracy: 93%

---

## Model Performance

| Metric    | Score |
|-----------|-------|
| F1 Score  | 0.93  |
| Precision | 0.96  |
| Recall    | 0.90  |
| Accuracy  | 93%   |

Trained on 3200 balanced samples from BigVul dataset (vulnerable / not vulnerable).

---

## Tech Stack

| Component        | Technology                                  |
|------------------|---------------------------------------------|
| ML Model         | CodeBERT (RobertaForSequenceClassification) |
| Training Data    | BigVul Dataset (20K+ real CVEs)             |
| Backend          | FastAPI + Uvicorn                           |
| Static Analysis  | Python + Regex                              |
| Chrome Extension | Vanilla JS (Manifest V3)                    |
| Deep Learning    | PyTorch + HuggingFace Transformers          |

---

## What BugFinder Catches That LeetCode Doesn't

LeetCode tells you about wrong answers and TLE after submission.
BugFinder tells you in real-time while you type:

- You have O(n^2) complexity BEFORE you submit
- You typed whil( instead of while(
- You have a missing closing brace
- You have unsafe memory access in C++ code
- Your non-void function has no return statement

---

## Project Structure
`
bugfinder/
├── analyzer/
│   └── static.py          # Rule-based static analyzer (12 checks)
├── model/
│   ├── predict.py          # ML inference function
│   └── saved/              # Fine-tuned CodeBERT checkpoint
├── data/
│   └── clean.csv           # Preprocessed balanced dataset
├── backend/
│   └── api.py              # FastAPI server
├── extension/
│   ├── manifest.json       # Chrome extension config
│   └── content.js          # Real-time content script
├── train.py                # Training script with LR scheduler
├── preprocess.py           # Data preprocessing + balancing
└── tokenize_data.py        # Pre-tokenization for fast training
`

---

## Setup

### 1. Install dependencies
`ash
git clone https://github.com/siddhantvaibhav/bugfinder
cd bugfinder
python -m venv venv
venv\Scripts\activate
pip install torch transformers fastapi uvicorn pandas scikit-learn datasets
`

### 2. Start the backend
`ash
uvicorn backend.api:app --reload
`

### 3. Load Chrome extension
- Go to chrome://extensions
- Enable Developer mode
- Click Load unpacked
- Select the extension/ folder

### 4. Open LeetCode
- Open any C++ problem
- Start typing code
- BugFinder panel appears automatically in bottom right

---

## What I Learned

- Fine-tuning transformer models on domain-specific vulnerability data
- Handling class imbalance in real-world CVE datasets
- Combining rule-based and ML approaches for better coverage
- Building end-to-end ML pipelines from data to deployment
- Chrome extension development with real-time API calls
- PyTorch training with learning rate scheduling and model checkpointing
