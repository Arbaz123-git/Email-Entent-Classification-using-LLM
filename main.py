import json 
from intent_classification import classify_email 
from email_preprocessing import preprocess_email

def main():
    print("Real Estate Email Intent Classification System")
    print("-----------------------------------------------")

    # In a real system, this will come from an email API or user input 
    email_text = input("Enter the email text to classify (or 'quit' to exit):\n")

    while email_text.lower() != 'quit':
        try:

            # Apply preprocessing and classification
            processed_email = preprocess_email(email_text)

            print("\n--- Classification Results ---")
            print("\n--- Email Preprocessing Results ---")

            print(f"Subject: {processed_email.subject}")
            print(f"Metadata extracted: {json.dumps(processed_email.metadata, indent=2)}")
            print(f"Paragraph Count: {len(processed_email.paragraphs)}")
            
            # Classify the email using preprocessed text
            result = classify_email(email_text)

            print("\n--- Classification Results ---")
            print(f"Primary Intent: {result.primary_intent}")

            if result.secondary_intents:
                print(f"Secondary Intents: {', '.join(str(intent) for intent in result.secondary_intents)}")
            else:
                print("Secondary Intents: None")

            print(f"Overall Confidence: {result.overall_confidence:.2f}")

            print("\nIntent Details:")
            for detail in result.intent_details:
                print(f"  • {detail.intent} (Confidence: {detail.confidence:.2f})")
                print(f"    Key Actions:")
                for action in detail.key_actions:
                    print(f"      - {action}")

            print(f"\nPriority: {result.priority}")
            print(f"Key Information")
            for item in result.key_information:
                print(f"  - {item}")

            print(f"Entities Mentioned: {', '.join(result.entities_mentioned)}")
            print(f"Suggested Action: {result.suggested_action}")
            print(f"Specialist Required: {', '.join(result.specialists_required)}")
            print(f"Estimated Completion Time: {result.estimated_completion_time}")
            print(f"Attachment Mentioned: {'Yes' if result.attachments_mentioned else 'No'}")
            print(f"Follow-up Required: {'Yes' if result.follow_up_required else 'No'}")

            # Output JSON for system integration 
            print("\nJSON Outout for system integration:")
            print(result.model_dump_json(indent=2))

        except Exception as e:
            print(f"Error: {e}")

        email_text = input("\nEnter the email text to classify (or 'quit' to exit):\n")

if __name__ == "__main__":
    main()
