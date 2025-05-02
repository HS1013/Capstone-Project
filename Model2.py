

from transformers import pipeline
import re
from typing import Dict, List, Tuple

class PIIAwareSummarizer:
    def __init__(self, model_name="Falconsai/text_summarization"):
        """
        Initialize the summarization pipeline with PII detection capabilities.
        
        Args:
            model_name: Name of the summarization model (default: Falconsai/text_summarization)
        """
        self.summarizer = pipeline("summarization", model=model_name)
        
        # Define regex patterns for common PII types
        self.pii_patterns = {
            "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "PHONE": r'(\+\d{1,2}\s?)?(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}\b',
            "ACCOUNT ID": r'\b(?:\d[ -]*?){13,16}\b',
            #"SSN": r'\b\d{3}-\d{2}-\d{4}\b',
            "BIRTHDATE": r'\b\d{4}-\d{2}-\d{2}\b',
            #"PERSON": r'([A-Z]+(?:\s[A-Z]+)+)',  # Simple name pattern
        }
        
    def detect_pii(self, text: str) -> Tuple[List[Dict], str]:
        """
        Detect PII entities in the input text using regex patterns.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple containing (list of detected entities)
        """
        entities = []
        anonymized_text = text
        
        for pii_type, pattern in self.pii_patterns.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    "entity_type": pii_type,
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end()
                })
        
        return entities
    
    def summarize_with_pii_awareness(self, text: str, **summarizer_kwargs) -> Dict:
        """
        Summarize text with PII awareness.
        
        Args:
            text: Input text to summarize
            summarizer_kwargs: Additional arguments for the summarization pipeline
            
        Returns:
            Dictionary containing:
            {
                "summary": generated summary,
            }
        """
        # Detect and anonymize PII
        pii_entities = self.detect_pii(text)
        
        # Generate summaries
        original_summary = self.summarizer(text, **summarizer_kwargs)[0]['summary_text']
        #anonymized_summary = self.summarizer(anonymized_text, **summarizer_kwargs)[0]['summary_text']
        
        return {
            "summary": original_summary,
            "pii_entities": pii_entities,
            #"anonymized_text": anonymized_text,
            #"anonymized_summary": anonymized_summary
        }


# Example usage
if __name__ == "__main__":
    # Initialize the PII-aware summarizer
    pii_summarizer = PIIAwareSummarizer()
    
    # Example text containing PII - insert downloaded data here in sentence format
    sample_text = """
    

    """
    
    # Get summary with PII information
    result = pii_summarizer.summarize_with_pii_awareness(
        sample_text,
        max_length=150,
        min_length=30,
        do_sample=False
    )
    
    print("=== Original Summary ===")
    print(result["summary"])
    
    #print("\n=== Anonymized Summary ===")
    #print(result["anonymized_summary"])
    
    print("\n=== Detected PII Entities ===")
    for entity in result["pii_entities"]:
        print(f"{entity['entity_type']}: {entity['value']}")

