# BTU_IR

Terminal-based application for processing and searching document collections with information retrieval capabilities.

_*This project is a part of the Information Retrieval Course taught at BTU Cottbus-Senftenberg._

## Features

- **Interactive CLI**: A user-friendly menu-driven interface for easy operation.
- **Dynamic Document Parsing**: Fetch and parse text collections from any URL. Users can define document boundaries using line numbers and regular expressions.
- **Multiple Search Algorithms**:
  - **Linear Boolean Search**: Simple term matching.
  - **TF-IDF Vector Space Search**: Ranked retrieval based on term relevance.
- **Flexible Stopword Removal**:
  - **List-based**: Filter common words using a default list or a user-provided file.
  - **Frequency-based**: Dynamically identify and remove terms that are either too common or too rare across the collection.
- **Search Evaluation**: For pre-configured demo cases, the system calculates and displays precision and recall scores against a ground truth dataset.
- **Porter Stemmer**: Includes a backend implementation of the Porter Stemming algorithm to reduce words to their root form.
- **Demo Mode**: Quickly load and test the system with pre-configured collections like **Aesop's Fables** or **Grimms' Fairy Tales**.

## Requirements

- Python 3.10+
- No external libraries required.

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
Enter search term: fox
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
└── test_wrapper.py     # Test wrapper
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
