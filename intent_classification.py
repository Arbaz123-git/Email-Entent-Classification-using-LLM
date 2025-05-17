# Step 1: Import necessary Libraries 

from enum import Enum 
from typing import List, Optional 
from pydantic import BaseModel, Field 
import instructor
import os
import json 
from groq import Groq

from system_prompt import ENHANCED_SYSTEM_PROMPT
from email_preprocessing import preprocess_email, ProcessedEmail

from dotenv import load_dotenv 

# load .env into environment 
load_dotenv()

# grab the key 
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY not found in environment")

# Step 2: Patch your LLM with instructor 

# Instructor makes it easy to get structured data like JSON from LLMs 

client = instructor.patch(Groq(api_key=api_key))

# Step 3: Define Pydantic data models 

class EmailIntent(str, Enum):
    LEASE_ABSTRACTION = "intent_lease_abstraction"
    COMPARISON_LOI_LEASE = "intent_comparison_loi_lease"
    CLAUSE_PROTECT = "intent_clause_protect"
    COMPANY_RESEARCH = "intent_company_research"
    TRANSACTION_DATE_NAVIGATOR = "intent_transaction_date_navigator"
    AMENDMENT_ABSTRACTION = "intent_amendment_abstraction"
    SALES_LISTINGS_COMPARISON = "intent_sales_listings_comparison"
    LEASE_LISTINGS_COMPARISON = "intent_lease_listings_comparison"

class EmailPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class IntentDetails(BaseModel):
    """Details about a specific intent identified in the email"""
    intent: EmailIntent 
    confidence: float = Field(ge=0, le=1, description="Confidence score for this intent")
    key_actions: List[str] = Field(description="Specific actions needed for this intent")

class EmailClassification(BaseModel):
    """Complete classification of an email, potentially with multiple intents"""
    primary_intent: EmailIntent
    secondary_intents: List[EmailIntent] = Field(default_factory=list, description="Additional intents identified in the email")
    intent_details: List[IntentDetails] = Field(description="Detailed information about each identified intent")
    priority: EmailPriority 
    overall_confidence: float = Field(ge=0, le=1, description="Overall confidence score for the classification")
    key_information: List[str] = Field(description="List of key points extracted from the email")
    entities_mentioned: List[str] = Field(description="Properties, companies, or people mentioned")
    suggested_action: str = Field(description="Brief suggestion for handling the email")
    specialists_required: List[str] = Field(description="Type of specialists best suited to handle this request")
    estimated_completion_time: str = Field(description="Estimated time needed to complete the request")
    attachments_mentioned: bool = Field(description="Whether the email mentions attachments")
    follow_up_required: bool = Field(description="Whether follow-up will likely be needed")

# Step 4: Define the classification function 

def classify_email(email_text: str, use_preprocessing: bool = True) -> EmailClassification:
    """  
    Classifies real estate emails using the GROQ LLama-3.3-70b-versatile model
    and returns structured information with support for multiple intents.

    Args:
        email_text: The content of the email to classify 
        use_preprocessing: Whether to apply email preprocessing (default: True)

    Returns:
        EmailClassification object with primary and secondary intents and other relevant information

    """
    try:
        # Preprocess the email if requested
        if use_preprocessing:
            processed_email = preprocess_email(email_text)
            # Use the cleaned text for classification
            text_for_classification = processed_email.clean_text
            
            # Print preprocessing info for debugging
            print(f"[Debug] Email preprocessing applied.")
            print(f"[Debug] Subject extracted: {processed_email.subject}")
            print(f"[Debug] Metadata extracted: {json.dumps(processed_email.metadata, indent=2)}")
        else:
            text_for_classification = email_text
            print("[Debug] Email preprocessing skipped.")
        
        # Make the API call with preprocessed text
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            response_model=EmailClassification,
            temperature=0.1,  # Lower temperature for more consistent outputs
            max_completion_tokens=1024,
            messages=[
                {
                    "role": "system",
                    "content": ENHANCED_SYSTEM_PROMPT,
                },
                {"role": "user", "content": text_for_classification}
            ]
        )
        
        # If preprocessing was used, we can enhance the result with metadata
        if use_preprocessing and hasattr(processed_email, 'metadata'):
            # We could override certain fields based on metadata
            # For example, update attachments_mentioned if detected in preprocessing
            if processed_email.metadata.get("has_attachments"):
                response.attachments_mentioned = True
                
            # Enhance entities if needed (could merge entities from preprocessing)
            # This is optional as the LLM should already detect entities
            
            # Update priority if urgent indicators were found
            if processed_email.metadata.get("urgent_indicators") and response.priority != EmailPriority.URGENT:
                # Consider upgrading priority if urgent indicators were found
                if response.priority == EmailPriority.LOW:
                    response.priority = EmailPriority.MEDIUM
                elif response.priority == EmailPriority.MEDIUM:
                    response.priority = EmailPriority.HIGH
        
        return response
    
    except Exception as e:
        print(f"Error during email classification: {str(e)}")
        # Re-raise or handle the error according to your application's needs
        raise
    