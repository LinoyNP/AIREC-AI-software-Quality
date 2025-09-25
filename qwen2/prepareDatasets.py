# Import standard library modules
from pathlib import Path  # For handling file paths in a clean, cross-platform way
import json               # To read/write JSON or JSONL files

# Import datasets library from Hugging Face
from datasets import load_dataset  
# load_dataset automates downloading, caching, and loading datasets from HF Hub
# It's different from pandas.read_csv:
# - pandas.read_csv reads a CSV file from local disk or URL
# - load_dataset can handle multiple formats (JSON, CSV, Parquet) and automatically returns a Dataset object
# - Provides easy access to train/test splits, metadata, etc.

# Define the main project directory (directory of this script)
THIS_DIR = Path(__file__).resolve().parent
# __file__ is the path to this script
# resolve() converts to an absolute path
# parent gives the folder containing the script

# ----------------------------
# Define project directories
# ----------------------------
DATASETS_DIR = THIS_DIR / "datasets"        # Root folder for all datasets
RAW_DIR = DATASETS_DIR / "raw"              # Folder for raw/unprocessed data
PROCESSED_DIR = DATASETS_DIR / "processed"  # Folder for processed/ready-to-train data

# Ensure folders exist before saving any files
# mkdir() works on Windows too with pathlib
# parents=True creates intermediate directories if they don't exist
# exist_ok=True prevents errors if the folder already exists
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Function to save dataset to JSONL
# ----------------------------
def save_jsonl(dataset, filename):
    """
    Save a dataset (HF Dataset or list of dicts) to JSONL format.
    Each row becomes a separate JSON line.
    """
    out_path = PROCESSED_DIR / filename
    with open(out_path, 'w', encoding='utf-8') as f:
        for example in dataset:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")
    print(f"Saved {len(dataset)} examples to {out_path}")

# ----------------------------
# FLAG: Use sample (True) or full dataset (False)
# ----------------------------
USE_SAMPLE = True  # Change to False when ready for full training

# ----------------------------
# 1️⃣ Code Readability Dataset (HF Hub)
# ----------------------------
if USE_SAMPLE:
    # Only 50 examples for local testing
    readability = load_dataset("se2p/code-readability-krod", split="train[:50]")
    save_jsonl(readability, "code_readability_sample.jsonl")
else:
    # Full dataset for cloud training
    readability = load_dataset("se2p/code-readability-krod", split="train")
    save_jsonl(readability, "code_readability_full.jsonl")

# ----------------------------
# 2️⃣ QuixBugs Dataset (Correctness)
# ----------------------------
if USE_SAMPLE:
    quix_sample = [
        {"code": "def add(a, b): return a + b", "label": "correct"},
        {"code": "def sub(a, b): return a + b", "label": "incorrect"}
    ]
    save_jsonl(quix_sample, "quix_sample.jsonl")
else:
    # Replace this with full download/clone + parsing
    # Example:
    # - Clone the repo: git clone https://github.com/jkoppel/QuixBugs.git
    # - Parse all files into list of dicts
    pass

# ----------------------------
# 3️⃣ CWE-Bench Java (Security)
# ----------------------------
if USE_SAMPLE:
    cwe_sample = [
        {"code": "String s = null; s.length();", "label": "vulnerable"},
        {"code": "int x = 0; x++;", "label": "safe"}
    ]
    save_jsonl(cwe_sample, "cwe_sample.jsonl")
else:
    # Full CWE-Bench parsing code here
    pass

# ----------------------------
# 4️⃣ Defects4J (Correctness)
# ----------------------------
if USE_SAMPLE:
    defects_sample = [
        {"code": "int divide(int a, int b) { return a / b; }", "label": "correct"},
        {"code": "int divide(int a, int b) { return a / 0; }", "label": "incorrect"}
    ]
    save_jsonl(defects_sample, "defects_sample.jsonl")
else:
    # Full Defects4J parsing code here
    pass

print("✅ Dataset processing completed.")