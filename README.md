# BTU_IR

Terminal-based application for processing and searching document collections with advanced stopword filtering capabilities.

_*This project is a part of Information Retreival Course taught in BTU Cottbus-Senftenberg_

## Features
- 📥 Download & parse text collections from URLs using regex patterns
- 📚 View parsed documents with metadata (author, origin, content preview)
- 🔍 Perform boolean search across documents
- 🛑 Stopword removal using:
  - Predefined stopword lists (`helpers/stopwords.txt`)
  - Frequency-based filtering (JC Crouch method)

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
Source URL: http://www.gutenberg.org/files/1342/1342-0.txt  # Pride and Prejudice
Start line: 200
End line: [Enter]
Story Separator: r"CHAPTER \d+\.?\n\n([A-Z ]+)\n\n"
Author: Jane Austen
Origin: Project Gutenberg
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
├── data/            # Sample datasets (gutenberg.json)
├── helpers/         # NLP utilities
│   └── stopwords.txt
├── public_tests/    # Test suites
│   ├── test_pr02_t2.py
│   ├── test_pr02_t3.py
│   └── test_pr02_t4.py
├── document.py      # Document class definition
├── main.py          # Terminal UI implementation
├── my_module.py     # Core IR functionality
└── test_wrapper.py  # Test harness
```

## Testing
```bash
# Install pytest
python -m pip install pytest

# Run all tests
python -m pytest public_tests/
```

## Virtual Environment Setup
```bash
python3.10 -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/MacOS
```
