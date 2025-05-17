import json 
import time 

from intent_classification import classify_email
from email_preprocessing import preprocess_email

# Collection of increasingly complex emails for testing
test_emails = [
    {
        "name": "Simple single intent email",
        "content": """Subject: Office Lease Review
Can someone please review the 400 Main Street office lease and flag any concerning clauses? 
We need to respond by Friday.
Thanks,
Sarah"""
    },
    {
        "name": "Email with formatting issues",
        "content": """FWD: Lease Review Needed ASAP
--------------------------
From: client@example.com
Sent: Tuesday, May 14, 2025
To: team@ourcompany.com
--------------------------

Hi there,

Please review attached lease for our new downtown location.
Need urgent feedback on the renewal terms.

Regards,
Client
--------------------------
This email and any files transmitted with it are confidential..."""
    },
    {
        "name": "Complex multi-intent email with numbered items",
        "content": """Subject: Multiple Action Items – Urgent Review Needed
Hi team,
We have a few high-priority tasks that need immediate attention:
1. The lease amendment for the Jackson Heights retail space just came in (attached). Please abstract it and identify any changes from the original lease, especially around rent escalations and renewal clauses.
2. For the Riverfront Lofts acquisition, I need a complete schedule of critical dates (inspection period, loan contingency, and closing) by tomorrow morning. The seller is requesting to move up the closing date.
3. Someone from legal should review the draft lease for the 5th Avenue office. It's missing indemnity protections, and the assignment clause seems overly broad—please flag any red flags.
Also, loop in research to run a background check on "Evergreen Property Holdings"—we need to understand their portfolio, principals, and whether they've been involved in any litigation in the past five years.
Let me know who's taking the lead on each item.
Thanks,
Morgan"""
    },
    {
        "name": "Email with HTML formatting",
        "content": """Subject: <b>URGENT</b>: Lease Comparison Needed

<div style="font-family: Arial, sans-serif;">
<p>Dear Real Estate Team,</p>

<p>I need a thorough comparison between the original LOI and the final lease agreement for the <i>Westside Plaza</i> property. The tenant is claiming discrepancies in the following areas:</p>

<ul>
<li>Base rent calculations</li>
<li>Common area maintenance charges</li>
<li>Sublease provisions</li>
</ul>

<p>Please highlight any <span style="color:red;">material differences</span> between the documents.</p>

<p>Regards,<br>
Jessica</p>
</div>"""
    },
    {
        "name": "Email with ambiguous and implicit intents",
        "content": """Subject: Follow-up on Parkview Building
Hey,
I met with the Parkview team yesterday. They're going to need us to look at their financial position before we finalize anything. Can we also check if they've been involved in any lawsuits recently? 

The deal structure we discussed also needs some work - the timing doesn't align with our investment strategy. Let's make sure we have all the key dates lined up correctly.

By the way, the agreement doesn't mention anything about maintenance responsibilities - we should probably fix that.

Chat soon,
Alex"""
    },
    {
        "name": "Multi-line subject and complex formatting",
        "content": """Subject: URGENT: Need Lease Review for Wilson Properties
       Industrial Space (Potential Red Flags Identified) - Response 
       Required by EOD Tomorrow

Team,

After a preliminary review of the Wilson Properties industrial lease that was sent 
over yesterday (see attached PDF), I'm concerned about several aspects that need 
immediate attention:

• Indemnification clause appears one-sided
• Operating expenses pass-through contains no cap
• Restoration requirements at lease end seem excessive
• No protection against adjacent tenant activities

The client needs our response by tomorrow afternoon for their board meeting.

Can someone please:

1. Perform a complete abstract of the lease
2. Highlight the problematic clauses mentioned above
3. Suggest alternative language for each issue

The Leasing Committee will meet at 2 PM tomorrow, so we need this completed
by noon at the latest.

Thanks in advance,

David Johnson
Senior Leasing Director
Commercial Property Advisors
Office: (555) 123-4567
Cell: (555) 987-6543
djohnson@cpadvisors.com"""
    },
    {
        "name": "Email with multi-paragraph descriptions and bullet points",
        "content": """Subject: Multiple Lease Listings Analysis for Expansion Options

Hi Team,

As we discussed in yesterday's expansion committee meeting, we need to assess multiple lease
options for our client's West Coast operations. They're looking to consolidate three separate
locations into one larger facility with the following requirements:

• Minimum 50,000 square feet
• Class A or B office space
• Access to public transportation
• On-site amenities (cafeteria preferred)
• Parking ratio of at least 3:1000
• Available for occupancy by Q3 2025

I've attached listings from three different brokers (CBRE, JLL, and Cushman) that each contain
5-7 potential properties. We need a comprehensive comparison of these listings focusing on:

1. Match with client requirements (ranked by % match)
2. Economic terms (base rent, escalations, concessions)
3. Hidden costs (operating expenses, tax exposure)
4. Flexibility options (expansion rights, termination options)

The economic analysis is particularly important, as some listings show very attractive base
rents but have concerning language about operating expense pass-throughs that could significantly
increase the effective occupancy costs.

Additionally, can someone verify the ownership structure of the Lakefront Tech Campus property?
There are rumors that the current owner might be involved in a merger that could affect
property management.

Let's coordinate a call for Thursday to review the findings. Please indicate your availability.

Best regards,

Sarah Williams
Director of Corporate Services
"""
    }
]

def run_tests():
    """Run tests on all test emails and report results"""

    print("Testing Email Preprocessing and Classification System")
    print("===================================================\n")
    
    results = []

    for i, test_case in enumerate(test_emails):
        print(f"Test {i+1}: {test_case['name']}")
        print(f"{'=' * len(test_case['name'])}")
        print(f"Email content: {test_case['content'][:150]}...\n")
        
        try:
            # Time the preprocessing
            start_time = time.time()
            processed = preprocess_email(test_case['content'])
            preprocess_time = time.time() - start_time
            
            print("Preprocessing Results:")
            print(f"Subject: {processed.subject}")
            print(f"Metadata: {json.dumps(processed.metadata, indent=2)}")
            print(f"Paragraph Count: {len(processed.paragraphs)}")

            print(f"Preprocessing Time: {preprocess_time:.2f} seconds\n")

            # Display how paragraphs were preserved
            print("First few paragraphs:")
            for idx, para in enumerate(processed.paragraphs[:3]):
                if idx > 0:
                    print("-----")
                print(para[:100] + ("..." if len(para) > 100 else ""))
            print("\n")

            # Show the clean text with preserved structure
            print("Clean text (first 300 chars):")
            print(processed.clean_text[:300] + "...")
            print("\n")

            # Time the classification
            start_time = time.time()
            result = classify_email(test_case['content'])
            classification_time = time.time() - start_time
            
            print("Classification Results:")
            print(f"Primary Intent: {result.primary_intent}")
            
            if result.secondary_intents:
                print(f"Secondary Intents: {', '.join(str(intent) for intent in result.secondary_intents)}")
            else:
                print("Secondary Intents: None")
            
            print(f"Priority: {result.priority}")
            print(f"Overall Confidence: {result.overall_confidence:.2f}")
            print(f"Classification Time: {classification_time:.2f} seconds\n")

            # Store the results for summary
            results.append({
                "name": test_case["name"],
                "success": True,
                "primary_intent": result.primary_intent,
                "secondary_intents": result.secondary_intents,
                "priority": result.priority,
                "confidence": result.overall_confidence,
                "preprocess_time": preprocess_time,
                "classification_time": classification_time,
                "paragraph_count": len(processed.paragraphs)
            })
            
        except Exception as e:
            print(f"Error processing email: {str(e)}\n")
            results.append({
                "name": test_case["name"],
                "success": False,
                "error": str(e)
            })
        
        print("-" * 50 + "\n")
    
    # Print summary
    print("\nTest Summary:")
    print("============")
    
    success_count = sum(1 for r in results if r["success"])
    print(f"Total Tests: {len(results)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(results) - success_count}")
    
    if success_count > 0:
        avg_preprocess = sum(r["preprocess_time"] for r in results if r["success"]) / success_count
        avg_classify = sum(r["classification_time"] for r in results if r["success"]) / success_count
        avg_paragraphs = sum(r["paragraph_count"] for r in results if r["success"]) / success_count

        print(f"\nAverage Preprocessing Time: {avg_preprocess:.2f} seconds")
        print(f"Average Classification Time: {avg_classify:.2f} seconds")
        print(f"Average Paragraph Count: {avg_paragraphs:.1f}")

    # Return results for potential further analysis
    return results

def test_multi_line_handling():
    """Specifically test the multi-line handling capability"""
    print("Testing Multi-line Text Handling")
    print("==============================\n")
    
    multi_line_test = """Subject: Quarterly Lease Review
          and Portfolio Analysis

Hello Real Estate Team,

I need two things completed by next Friday:

1. A complete review of the attached lease for 
   the Westfield Corporate Center. Please focus
   on identifying any unusual clauses, especially
   regarding the tenant improvement allowance
   and renewal options.

2. An updated transaction schedule for our Q2
   closings. The executive team needs this for
   the board presentation.

Also, can someone verify whether the Henderson
Tower transaction includes the adjacent parking
structure? The documentation is unclear on this
point.

Thanks!
Jennifer"""
    
    print("Original multi-line email:")
    print("-------------------------")
    print(multi_line_test)
    print("\n")
    
    # Process the multi-line email
    processed = preprocess_email(multi_line_test)
    
    print("Preprocessing Results:")
    print("--------------------")
    print(f"Subject: {processed.subject}")
    print(f"Metadata: {json.dumps(processed.metadata, indent=2)}")
    print(f"Paragraph Count: {len(processed.paragraphs)}")
    
    print("\nCleaned text (preserved structure):")
    print("----------------------------------")
    print(processed.clean_text)
    
    print("\nParagraphs extracted:")
    print("-------------------")
    for i, para in enumerate(processed.paragraphs):
        print(f"Paragraph {i+1}: {para}")
    
    return processed


if __name__ == "__main__":
    # Run all tests
    print("=== RUNNING FULL TEST SUITE ===\n")
    run_tests()
    
    print("\n\n=== SPECIFICALLY TESTING MULTI-LINE HANDLING ===\n")
    test_multi_line_handling()