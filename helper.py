def read_multiline(prompt="Enter your full email (end with a line containing '__END__'):"):
    """
    Reads multiple lines from stdin until a sentinel line ('__END__') is encountered.
    Returns the concatenated string of all lines (excluding the sentinel).
    """
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            # In case of EOF, break out 
            break 
        if line.strip() == "__END__":
            break 
        lines.append(line)
    return "\n".join(lines)

def display_classification(result):
    """Print structured classification results to console"""
    print("\n--- Classification Results ---")
    print(f"Primary Intent: {result.primary_intent}")
    if result.secondary_intents:
        sec = ', '.join(str(i) for i in result.secondary_intents)
        print(f"Secondary Intents: {sec}")
    else:
        print("Secondary Intents: None")
    print(f"Overall Confidence: {result.overall_confidence:.2f}\n")

    print("Intent Details:")
    for detail in result.intent_details:
        print(f"  • {detail.intent} (Confidence: {detail.confidence:.2f})")
        print("    Key Actions:")
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

