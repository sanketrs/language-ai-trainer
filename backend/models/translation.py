from transformers import MarianMTModel, MarianTokenizer

# Load MarianMT model for English to Marathi translation
model_name = "Helsinki-NLP/opus-mt-en-mr"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_to_marathi(english_text):
    # Tokenize the input text with PyTorch tensors
    inputs = tokenizer(english_text, return_tensors="pt", padding=True)
    input_ids = inputs["input_ids"]  # Extract input IDs
    # Generate translation
    translated = model.generate(input_ids)
    # Decode translated tokens into Marathi text
    marathi_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return marathi_text

