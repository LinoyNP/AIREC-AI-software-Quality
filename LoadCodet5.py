# This file is responsible for loading the CodeT5-small model for offline use.
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

# Folder to store the model locally
local_folder = "./codet5-small"
MODEL_NAME = "Salesforce/codet5-small"

# only for the first time
if not os.path.exists(local_folder) or not os.listdir(local_folder):
    print("Downloading CodeT5-small model for the first time...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    tokenizer.save_pretrained(local_folder)
    model.save_pretrained(local_folder)
else:
    # offline
    tokenizer = AutoTokenizer.from_pretrained(local_folder, local_files_only=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(local_folder, local_files_only=True)

print("CodeT5-small loaded and ready for offline use!")