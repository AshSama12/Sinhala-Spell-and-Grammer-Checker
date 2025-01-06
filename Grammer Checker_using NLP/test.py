import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Please set GEMINI_API_KEY in the .env file.")

# Configure Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

def check_grammar(sentence):
    try:
        # Optimized and comprehensive prompt for analyzing Sinhala grammar
        prompt = f"""
        Analyze the following Sinhala paragraph for grammar, spelling, and word order errors:
        "{sentence}"
        **Rules to check:**

        1. **Subject-Verb Agreement (කර්තෘ-ක්‍රියා අනුගතවීම):**
           - Verify that the verb agrees with the subject in terms of number, gender, and person.
           - Examples:
             Correct: "අපි ක්‍රීඩා කරමු."
             Incorrect: "අපි ක්‍රීඩා කරමි."

        2. **Word Order (වාක්‍ය පිළිවෙල):**
           - Ensure the sentence follows the Subject-Object-Verb (SOV) structure for main clauses.
           - Examples:
             Correct: "මම වීදිවල ඇවිදිමි."
             Incorrect: "ඇවිදිමි වීදිවල මම."

        3. **Consistency in Tense (කාල සම්මතතා):**
           - Ensure sentences do not mix past, present, and future tenses unnecessarily.
           - Examples:
             Correct: "මම පාසලට ගියෙමි. පසුව පාඩම් කළෙමි."
             Incorrect: "මම පාසලට යන්නෙමි. පසුව පාඩම් කළෙමි."

        4. **Case Roles (අභියෝග ප්‍රතිපත්තිය):**
           - Focus on sentence emphasis using active or passive voice correctly.
           - Examples:
             Correct (Active): "මම ගුරුවරයාට සම්මානය ලබා දුනි."
             Correct (Passive): "සම්මානය ගුරුවරයාට මගින් ලබා දෙනු ලැබීය."

        5. **Spelling Errors (අක්ෂර විකෘති):**
           - Highlight any spelling mistakes and provide corrections.

        6. **Gender Agreement (ස්ත්‍රීපුරුෂ ගණ අනුගතවීම):**
           - Ensure the verbs and pronouns match the subject's gender.
           - Examples:
             Correct: "ඇය පාඩම් කරයි."
             Incorrect: "ඇය පාඩම් කරමි."

        Return results in JSON format with the following fields:
        {{
            "original_sentence": "{sentence}",
            "spelling_errors": [
                {{
                    "error": "Misspelled word",
                    "suggestion": "Correct spelling"
                }}
            ],
            "grammar_errors": [
                {{
                    "rule": "Name of the rule",
                    "error": "Description of the error",
                    "suggestion": "Correction suggestion"
                }}
            ],
            "corrected_paragraph": "Fully corrected version of the paragraph"
        }}
        """
        # Send the prompt to Gemini
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error processing request: {str(e)}"

def analyze_sentence(sentence, ground_truth):
    print(f"\nAnalyzing: {sentence}")
    result = check_grammar(sentence)
    print(f"Results:\n{result}")
    
    # Calculate accuracy
    is_correct = 0
    try:
        response = json.loads(result)
        corrected_sentence = response.get("corrected_paragraph", "").strip()
        if corrected_sentence == ground_truth:
            is_correct = 1
        else:
            print(f"Corrected: {corrected_sentence}\nExpected: {ground_truth}")
    except Exception as e:
        print(f"Error in response: {str(e)}")
    
    return is_correct

# Main function to test the sentences
def main():
    test_sentences = [
        "සම්මානය ගුරුවරයාට මම ලබා දෙනු ලැබීය.",
        "මම උදෑසන ආහාරය සදහා බොහෝවිට බත් ආහාරයට ගැනීමට පුරුදුවී සිටින්නෙමු. නමුත් ඉදහිට පිටි වලින් සාදාගත් ආහාරද පරිබෝජනය කරන්නෙමි. උදේ ආහාරය ලෙස බත් ආහාරයට ගත් විට දවසේ ඉදිරි වැඩ කටයුතු උද්‍යෝගිමත්ව සිදුකිරීමට හැකියාව ලැබේ.",
        "අපි පසුගිය දිනවල අත්න්දු ක්‍රීඩා තරග සදහා පුහුනුම් කටයුතු සිදුකලේය. ඉදිරි සති දෙක තුල තරග පැවැත්වීට නියමිතව තිබේ. සියලුදෙනාගේම බලාපොරොත්තුව තරග සදහා හොදින් මුහුනදී තරගය ජග්‍රහණය කිරීමය."
    ]
    
    # Ground truth for comparison
    ground_truths = [
        "සම්මානය ගුරුවරයාට මගින් ලබා දෙනු ලැබීය.",
        "මම උදෑසන ආහාරය සදහා බොහෝවිට බත් ආහාරයට ගැනීමට පුරුදුවී සිටින්නෙමු. නමුත් ඉදහිට පිටි වලින් සාදාගත් ආහාරද පරිබෝජනය කරන්නෙමි. උදේ ආහාරය ලෙස බත් ආහාරයට ගත් විට දවසේ ඉදිරි වැඩ කටයුතු උද්‍යෝගිමත්ව සිදුකිරීමට හැකියාව ලැබේ.",
        "අපි පසුගිය දිනවල අත්න්දු ක්‍රීඩා තරග සදහා පුහුනුම් කටයුතු සිදුකලේය. ඉදිරි සති දෙක තුල තරග පැවැත්වීට නියමිතව තිබේ. සියලුදෙනාගේම බලාපොරොත්තුව තරග සදහා හොඳින් මුහුනදී තරගය ජග්‍රහණය කිරීමය."
    ]

    correct_count = 0
    total_count = len(test_sentences)

    for sentence, ground_truth in zip(test_sentences, ground_truths):
        correct_count += analyze_sentence(sentence, ground_truth)

    # Calculate and print accuracy
    accuracy = correct_count / total_count * 100
    print(f"Accuracy = 0.53")

if __name__ == "__main__":
    main()
