from intent_classification import classify_email

# Test with sample emails 

sample_emails = [
    """Hi team, Can you pull together a schedule of important dates for the escrow process on the 125 King St deal? We're especially concerned with closing and due diligence periods. Thanks!""",

    """Hey, I'm reviewing the lease on the 3rd Avenue property. Can you check if there are any red flags-like missing indemnity clauses or unfavourable assignment terms?""",

    """Please abstract the lease for the Johnson project (PDF attached). We need to know the base rent, commencement and expiry dates, renewal options, and escalation schedule.""",

    """Hi there, I have two requests: 1) Can you analyze the Madison Tower lease amendment to see what changed from the original agreement, and 2) We need to verify the closing date for the Lincoln property transaction. The escrow officer mentioned it might be moved up. Thanks!"""
]

# Example of how to process emails 
def process_email_batch(emails):
    """Process a batch of emails and print their classifications"""
    for i, email in enumerate(emails):
        print(f"\n--- Email {i+1} ---")
        print(f"Content: {email[:100]}...")

        try:
            result = classify_email(email)
            print(f"\nPrimary Intent: {result.primary_intent}")

            if result.secondary_intents:
                print(f"Secondary Intents: {', '.join(str(intent) for intent in result.secondary_intents)}")
            else:
                print("Secondary Intents: None")

            print(f"Overall Confidence: {result.overall_confidence:.2f}")
            print(f"Priority: {result.priority}")
            print(f"Key Information: {', '.join(result.key_information[:3])}...")  # Show just first 3 items 
            print(f"Suggested Action: {result.suggested_action}")
            print(f"Specialist Required: {', '.join(result.specialists_required)}")
        except Exception as e:
            print(f"Error classifying email: {e}")


process_email_batch(sample_emails)
