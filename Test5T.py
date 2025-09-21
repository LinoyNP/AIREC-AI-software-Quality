# Test5T.py
# ----------------------------
# Purpose: 
# This script tests the offline loading of the CodeT5-small model and gets a fix suggestion.
# It uses the LoadCodet5.py loader to access the model and tokenizer.
# ----------------------------

from LoadCodet5 import tokenizer, model

# Step 1: Define a sample piece of code with a small error
# We'll intentionally remove a closing parenthesis to see if the model can fix it.
sample_code = "fix: def add(a, b\n    return a + b"

# Step 2: Tokenize the input code
# Converts text into numerical tokens (PyTorch tensors)
inputs = tokenizer(sample_code, return_tensors="pt")

# Step 3: Generate model output
# The model processes the tokens and produces a corrected sequence.
outputs = model.generate(**inputs, max_length=50)  

# Step 4: Decode the output tokens back to text
decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Step 5: Print the model's response
print("Model suggested fix:\n", decoded_output)
