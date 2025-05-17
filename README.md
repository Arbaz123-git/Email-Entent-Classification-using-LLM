# Email-Entent-Classification-using-LLM

The Real Estate Email Intent Classification System automates the processing of incoming commercial real estate emails by extracting structured information and categorizing requests into predefined intent categories. It helps operations teams respond efficiently with accurate, prioritized actions.

Key features:

Email Preprocessing: Cleans and structures raw email text, extracts subjects, metadata (attachments, dates), and paragraphs.

Intent Classification: Uses a patched LLM (GROQ LLama-3.3-70b-versatile) to identify primary and secondary intents, confidence scores, priorities, key actions, and specialists required.

Interactive CLI: Provides a friendly interface for real-time, one-off classification of emails.

Modular CLI Framework: Supports batch processing, test suite execution, and special case testing through subcommands.

Extensible Design: Easily add new intent categories, refine system prompts, or integrate evaluation tools.

Intent Categories

1. Lease Abstraction: Extract lease metadata and clauses (rent, term, landlord, tenant, renewal options).

2. LOI vs Lease Comparison: Compare LOI (Letter of Intent) against final lease to spot deviations.

3. Clause Protection: Detect risky or missing lease clauses (subletting rights, break clauses).

4. Company Research: Gather company credibility, litigation history, portfolio.

5. Transaction Date Navigator: Extract, verify, or schedule important transaction dates (escrow, closing).

6. Amendment Abstraction: Highlight changes in lease amendments vs original agreement.

7. Sales Listings Comparison: Compare commercial sales listings across brokers.

8. Lease Listings Comparison: Compare lease listings against client requirements.

Installation

1. Clone the repository:

git clone https://github.com/your-org/real-estate-email-intent-classifier.git
cd real-estate-email-intent-classifier

2. Create a virtual environment:

python3 -m venv venv
source venv/bin/activate

3. Install dependencies:

pip install -r requirements.txt

4. Configure environment variables:

GROQ_API_KEY=your-groq-api-key

Project Structure

├── classify_sample_email.py     # Sample batch processor for demos
├── email_preprocessing.py       # Extracts metadata and structures email
├── intent_classification.py     # Pydantic models and classify_email() function
├── system_prompt.py             # System and few-shot prompts
├── test.py                      # Unit tests and multi-line handlers
├── evaluation.py                # (Optional) Evaluates test output
├── main.py                      # Interactive CLI mode (input loop)
├── interactive_cli.py           # Modular CLI with argument-based subcommands
├── requirements.txt             # Dependencies
└── README.md                    # Project documentation

Usage

1. Run Using Main CLI (interactive loop)

python main.py

Enter raw email text when prompted.

Outputs include preprocessing results, classification, JSON payload.

2. Use CLI with Subcommands

python interactive_cli.py <mode>

Supported Modes:

interactive: Run real-time classification with prompts

sample: Process batch of preloaded emails (from classify_sample_email.py)

test: Run unit tests from test.py

multiline: Check for paragraph and subject handling edge cases

Customization

Intent Definitions: Modify EmailIntent enum inside intent_classification.py.

Prompts & Behaviors: Edit system_prompt.py to control system and few-shot behavior.

Model Parameters: Adjust API temperature, max tokens, and retry logic inside classify_email().

