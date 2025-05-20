import json 
from intent_classification import classify_email 
from email_preprocessing import preprocess_email
from helper import read_multiline, display_classification

def main():
    print("Real Estate Email Intent Classification System")
    print("-----------------------------------------------")
    print("Type or paste your full email below. When finished, enter a line with __END__ to submit.\n")

    while True:
        email_text = read_multiline()
        if not email_text.strip():
            # Empty input, exit
            print("No input detected. Exiting.")
            break
        if email_text.strip().lower() == 'quit':
            print("Exiting interactive mode.")
            break

        try:
            # Preprocess
            processed_email = preprocess_email(email_text)
            print("\n--- Email Preprocessing Results ---")
            print(f"Subject: {processed_email.subject}")
            print(f"Metadata: {json.dumps(processed_email.metadata, indent=2)}")
            print(f"Paragraph Count: {len(processed_email.paragraphs)}")

            # Classify
            result = classify_email(email_text)
            display_classification(result)

        except Exception as e:
            print(f"Error during processing: {e}")

        print("\nEnter another email or 'quit' to exit.")


if __name__ == '__main__':
    main()
