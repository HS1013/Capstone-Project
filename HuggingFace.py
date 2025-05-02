
# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("summarization", model="Falconsai/text_summarization")
#pipe = pipeline("text-classification", model="Falconsai/text_summarization")

# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Falconsai/text_summarization")
model = AutoModelForSeq2SeqLM.from_pretrained("Falconsai/text_summarization")
