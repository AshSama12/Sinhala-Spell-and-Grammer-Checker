
!pip install tensorflow pandas numpy scikit-learn
from google.colab import drive
import pandas as pd

# Mount Google Drive
drive.mount('/content/drive')

# Load the dataset
file_path = '/content/drive/MyDrive/AI project/correct and wrong sentences .csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Display the first few rows of the dataset
print(df.head())
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Separate inputs (sentences) and labels
sentences = df.iloc[:, 0].tolist() + df.iloc[:, 1].tolist() + df.iloc[:, 2].tolist()
labels = [0] * len(df.iloc[:, 0]) + [1] * len(df.iloc[:, 1]) + [2] * len(df.iloc[:, 2])

# Tokenize sentences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
sequences = tokenizer.texts_to_sequences(sentences)

# Pad sequences to ensure uniform length
max_length = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post')

# Get vocabulary size
vocab_size = len(tokenizer.word_index) + 1
# Convert labels to one-hot encoding
from tensorflow.keras.utils import to_categorical
labels = to_categorical(labels, num_classes=3)
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)
# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

import re
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Define a function to tokenize Sinhala paragraphs into sentences
def sinhala_sent_tokenize(paragraph):
    # Custom sentence tokenizer for Sinhala
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', paragraph)
    return [s.strip() for s in sentences if s.strip()]

# Define a function to predict grammar correctness for each sentence
def predict_paragraph_with_detailed_errors(paragraph):
    # Split the paragraph into individual sentences
    sentences = sinhala_sent_tokenize(paragraph)

    # Store predictions for each sentence
    results = []
    for sentence in sentences:
        sequence = tokenizer.texts_to_sequences([sentence])
        padded_sequence = pad_sequences(sequence, maxlen=max_length, padding='post')
        prediction = model.predict(padded_sequence)[0]  # Get the probabilities for each class

        # Determine the type of error or correctness
        is_rule1_error = prediction[1] > 0.5  # Adjust threshold as needed
        is_rule2_error = prediction[2] > 0.5  # Adjust threshold as needed

        if not is_rule1_error and not is_rule2_error:
            prediction_label = "Correct Grammar"
        elif is_rule1_error and not is_rule2_error:
            prediction_label = "Wrong: Rule 1 Error"
        elif not is_rule1_error and is_rule2_error:
            prediction_label = "Wrong: Rule 2 Error"
        else:
            prediction_label = "Wrong: Both Rule 1 and Rule 2 Errors"

        # Store the result
        results.append({
            "sentence": sentence,
            "prediction": prediction_label
        })
    
    return results

# Test the function with a Sinhala paragraph
test_paragraph = "අපි ඔවුන් ප්‍රේම කරන දෙස බලා සිටියෙමු. අපි පොත් පාඩම් කලෙමු. ඔවුහු කති.ප්‍රේම කරන දෙස ඔවුන් බලා සිටියෙමු අපි. මම පන්සල් ගියෙමි. ඇය පන්සල් ගියෙමි. ඇය ගියෙමි. ඔවුහු ගෙදර යති"

# Get the results
results = predict_paragraph_with_detailed_errors(test_paragraph)

# Print the predictions for each sentence
for res in results:
    print(f"Sentence: {res['sentence']}
Prediction: {res['prediction']}
")
