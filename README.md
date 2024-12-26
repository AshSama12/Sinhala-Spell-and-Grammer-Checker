# Sinhala Grammar Correction System

This repository contains a rule-based Sinhala grammar correction system that analyzes a dataset of correct Sinhala sentences, generates grammatical rules, and applies them to correct user inputs.

## Features
- Extracts rules from a dataset of grammatically correct Sinhala sentences.
- Tokenizes and analyzes patterns (word frequencies and bigrams).
- Applies the extracted rules to correct user-entered paragraphs interactively.

## How It Works
1. **Dataset**: The system uses a dataset containing only correct Sinhala sentences (e.g., `grammerRule1.txt`).
2. **Rule Generation**: Analyzes tokenized sentences to identify word frequencies and bigram patterns.
3. **User Input**: Accepts a Sinhala paragraph from the user and applies the generated rules to provide corrections.

## Usage
1. Place your dataset file (`grammerRule1.txt`) in the project directory.
2. Run the script:
   ```bash
   python grammar_correction.py
   ```
3. Enter a Sinhala paragraph when prompted.
4. The corrected paragraph will be displayed.

## Dataset Format
- The dataset should contain only correct Sinhala sentences, one sentence per line.
- Example:
  ```
  මම පාසලට ගියා.
  අපි ගමේ වෙළඳසැලට ගියා.
  ```

## Requirements
- Python 3.7+
- Required libraries: `re`, `collections`, `sklearn`

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Project Structure
```
.
├── grammar_correction.py  # Main script
├── grammerRule1.txt       # Dataset of correct Sinhala sentences
└── README.md              # Project documentation
