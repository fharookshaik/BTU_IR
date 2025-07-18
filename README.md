# BTU_IR

Terminal-based application for processing and searching document collections with advanced information retrieval capabilities.

_*This project is a part of Information Retreival Course taught in BTU Cottbus-Senftenberg_

## Features
- 📥 Download & parse text collections from URLs using regex patterns
- 📚 View parsed documents with metadata (author, origin, content preview)
- 🔍 Perform searches using multiple algorithms:
  - **Linear Boolean Search**: Simple term matching.
  - **TF-IDF Vector Space Search**: Ranked retrieval based on term relevance.
- 🛑 Stopword removal using:
  - Predefined stopword lists (`helpers/stopwords.txt`)
  - Frequency-based filtering (JC Crouch method)
- 🌳 **Porter Stemming**: Reduces words to their root form for more effective searching.

## Requirements
- Python 3.10+
- Dependencies: None (standard library only)

## Installation
```bash
git clone https://github.com/fharookshaik/BTU_IR.git
cd BTU_IR
```

## Usage
```bash
python main.py
```

### Example Workflow
1. **Download & Parse:**
```python
Source URL: https://www.gutenberg.org/files/21/21-0.txt  # Aesop's Fables
Start line: 845
End line: 5953
Story Separator: r"([^\n]+)\n\n(.*?)(?=\n{5}(?=[^\n]+\n\n)|$)"
Author: Aesop
Origin: Aesops Fables
```

2. **Search Documents:**
```python
Enter search term: darcy
Results: 45 matches across documents
```

3. **Stopword Filtering:**
```python
Choose method: 2 (Frequency-based)
Common Frequency: 0.4
Rare Frequency: 0.05
```

## Project Structure
```
BTU_IR/
├── .gitignore
├── CHANGELOG.txt 
├── Levenshtein.py      # Levenshtein distance calculation
├── README.md
├── data/               # Sample datasets (gutenberg.json)
│   ├── gt_aesop.json
│   ├── gt_grimm.json
│   └── gutenberg.json
├── document.py         # Document class definition
├── helpers/            # NLP utilities
│   └── stopwords.txt
├── main.py             # Terminal UI implementation
├── my_module.py        # Core IR functionality
├── public_tests/       # Test suites
│   ├── englishST.txt
│   ├── test_pr02_t2.py
│   ├── test_pr02_t3.py
│   ├── test_pr02_t4.py
│   ├── test_pr03_t1.py
│   ├── test_pr03_t2.py
│   └── test_pr03_t3.py
├── task_3.py               
└── test_wrapper.py     # Test harness
```

## Testing
```bash
# Run all tests
python -m unittest discover -s public_tests/ -p "test_*.py"
```

## Virtual Environment Setup
```bash
python3.10 -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/MacOS
```
