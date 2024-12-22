from flask import Flask, request, jsonify
from rapidfuzz import process
import re
import pickle

app = Flask(__name__)

# Load the Sinhala dictionary
with open('sinhala_dictionary.txt', 'r', encoding='utf-8') as file:
    sinhala_words = set(file.read().splitlines())

# Function to tokenize Sinhala text
def tokenize_text(text):
    words = re.findall(r'[\u0D80-\u0DFF]+', text)  # Unicode range for Sinhala characters
    return words

# Function to check spelling
def check_spelling(tokens, dictionary):
    misspelled_words = []
    for word in tokens:
        if word not in dictionary:
            misspelled_words.append(word)
    return misspelled_words

# Function to suggest corrections for a word
def suggest_corrections(word, dictionary, limit=6):
    suggestions = process.extract(word, dictionary, limit=limit)
    return [match[0] for match in suggestions]

@app.route('/')
def home():
    return "Welcome to the Sinhala Spell Checker API"

@app.route('/check', methods=['POST'])
def check():
    input_text = request.form.get('text', '')  # Get the text input from the form
    
    # Tokenize the input text and check for spelling mistakes
    tokens = tokenize_text(input_text)
    misspelled_words = check_spelling(tokens, sinhala_words)
    
    suggestions = {}
    for word in misspelled_words:
        suggestions[word] = suggest_corrections(word, sinhala_words)
    
    return jsonify({
        'misspelled': misspelled_words,
        'suggestions': suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)
