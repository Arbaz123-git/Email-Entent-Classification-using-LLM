import argparse
import json
import sys

from intent_classification import classify_email
from email_preprocessing import preprocess_email

# Optional imports if these utility modules exist
try:
    from classify_sample_email import process_email_batch
except ImportError:
    process_email_batch = None

try:
    from test import run_tests, test_multi_line_handling
except ImportError:
    run_tests = None
    test_multi_line_handling = None

try:
    from evaluation import evaluate
except ImportError:
    evaluate = None


def interactive_mode():
    """Run interactive CLI for single email classification"""
    print("Real Estate Email Intent Classification System")
    print("-----------------------------------------------")

    while True:
        email_text = input("\nEnter the email text to classify (or 'quit' to exit):\n")
        if email_text.strip().lower() == 'quit':
            print("Exiting interactive mode.")
            break

        try:
            processed = preprocess_email(email_text)
            print("\n--- Email Preprocessing Results ---")
            print(f"Subject: {processed.subject}")
            print(f"Metadata: {json.dumps(processed.metadata, indent=2)}")

            result = classify_email(email_text)
            display_classification(result)

        except Exception as e:
            print(f"Error: {e}")


def sample_mode():
    """Process a batch of sample emails if available"""
    if process_email_batch is None:
        print("Sample batch processor not found. Ensure 'classify_sample_email.py' is available.")
        return
    samples = process_email_batch
    # process_email_batch itself prints results


def test_mode():
    """Run full test suite if available"""
    if run_tests is None:
        print("Test suite not found. Ensure 'test.py' is available.")
        return
    results = run_tests()
    if evaluate and isinstance(results, list):
        print("\n--- Evaluation Summary ---")
        evaluate(results)


def multiline_mode():
    """Run specific multi-line handling test if available"""
    if test_multi_line_handling is None:
        print("Multi-line test not found. Ensure 'test.py' is available.")
        return
    print("\n--- Multi-line Handling Test ---")
    processed = test_multi_line_handling()
    print(f"Processed subject: {processed.subject}")


def display_classification(result):
    """Prints structured classification results to console"""
    print("\n--- Classification Results ---")
    print(f"Primary Intent: {result.primary_intent}")
    if result.secondary_intents:
        sec = ', '.join(str(i) for i in result.secondary_intents)
        print(f"Secondary Intents: {sec}")
    else:
        print("Secondary Intents: None")

    print(f"Overall Confidence: {result.overall_confidence:.2f}")
    print("\nIntent Details:")
    for detail in result.intent_details:
        print(f"  • {detail.intent} (Confidence: {detail.confidence:.2f})")
        for action in detail.key_actions:
            print(f"      - {action}")

    print(f"\nPriority: {result.priority}")
    print("Key Information:")
    for info in result.key_information:
        print(f"  - {info}")

    print(f"Entities Mentioned: {', '.join(result.entities_mentioned)}")
    print(f"Suggested Action: {result.suggested_action}")
    print(f"Specialists Required: {', '.join(result.specialists_required)}")
    print(f"Estimated Completion Time: {result.estimated_completion_time}")
    print(f"Attachments Mentioned: {'Yes' if result.attachments_mentioned else 'No'}")
    print(f"Follow-up Required: {'Yes' if result.follow_up_required else 'No'}")

    print("\nJSON Output for system integration:")
    print(result.model_dump_json(indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Real Estate Email Intent Classification CLI"
    )
    subparsers = parser.add_subparsers(dest='command')

    # Interactive
    parser_inter = subparsers.add_parser('interactive', help='Interactive single email classification')

    # Sample batch
    subparsers.add_parser('sample', help='Run sample email batch classification')

    # Test suite
    subparsers.add_parser('test', help='Run full test suite')

    # Multi-line test
    subparsers.add_parser('multiline', help='Test multi-line handling specifically')

    args = parser.parse_args()

    if args.command == 'interactive':
        interactive_mode()
    elif args.command == 'sample':
        sample_mode()
    elif args.command == 'test':
        test_mode()
    elif args.command == 'multiline':
        multiline_mode()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
