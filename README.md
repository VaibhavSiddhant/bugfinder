# BugFinder — Real-Time C++ Bug Detector for LeetCode

A real-time C++ code analysis tool that detects bugs and vulnerabilities as you type on LeetCode. Combines static analysis with a fine-tuned CodeBERT model trained on real CVE data.

---

## Demo

The extension analyzes your C++ code every 3 seconds and shows a live panel with warnings.

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

### Static Analyzer (Rule-based)
- O(n^2) complexity detection — nested loop warning before submission
- Infinite loop risk detection — while(true) / while(1)
- Assignment in condition — if(x=5) instead of if(x==5)
- Array bounds risk — array access without size check
- Pointer safety — null dereference risk

### ML Model (CodeBERT)
- Fine-tuned microsoft/codebert-base on BigVul dataset
- 20,000+ real C/C++ CVEs from GitHub
- Binary classification: vulnerable / not vulnerable
- F1 Score: 0.91 | Accuracy: 91%

---

## Model Performance

| Metric    | Score |
|-----------|-------|
| F1 Score  | 0.91  |
| Precision | 0.99  |
| Recall    | 0.84  |
| Accuracy  | 91%   |

Trained on 800 balanced samples (vulnerable / not vulnerable) from BigVul dataset.

---

## Tech Stack

| Component        | Technology                        |
|------------------|-----------------------------------|
| ML Model         | CodeBERT (RobertaForSequenceClassification) |
| Training Data    | BigVul Dataset (20K+ CVEs)        |
| Backend          | FastAPI + Uvicorn                 |
| Static Analysis  | Python + Regex                    |
| Chrome Extension | Vanilla JS (Manifest V3)          |
| Deep Learning    | PyTorch + HuggingFace Transformers |

---

## Project Structure
`
bugfinder/
├── analyzer/
│   └── static.py          # Rule-based static analyzer
├── model/
│   ├── predict.py          # ML inference function
│   └── saved/              # Fine-tuned model checkpoint
├── data/
│   ├── bigvul.csv          # Raw BigVul dataset
│   └── clean.csv           # Preprocessed balanced dataset
├── backend/
│   └── api.py              # FastAPI server
├── extension/
│   ├── manifest.json       # Chrome extension config
│   └── content.js          # Content script
├── train.py                # Training script
├── preprocess.py           # Data preprocessing
└── tokenize_data.py        # Pre-tokenization for fast training
`

---

## Setup

### 1. Clone and install dependencies
`ash
git clone https://github.com/yourusername/bugfinder
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
- Open any problem
- Select C++ as language
- Start typing — BugFinder panel appears automatically

---

## Why This Project

LeetCode tells you about wrong answers and TLE after submission. BugFinder tells you:
- You have O(n^2) complexity BEFORE you submit
- You have unsafe memory access in your C++ code
- You have pointer dereference risks

This fills the gap between writing code and submitting it.

---

## What I Learned

- Fine-tuning transformer models on domain-specific code data
- Handling class imbalance in real-world vulnerability datasets
- Building end-to-end ML pipelines from data to deployment
- Combining rule-based and ML approaches for better results
- Chrome extension development with real-time API integration
