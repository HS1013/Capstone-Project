

from transformers import pipeline

summarizer = pipeline("summarization", model="Falconsai/text_summarization")

#Insert your downloaded data into ARTICLE and make sure the data is listed in full sentences and not in bullet point format

ARTICLE = """

"""

#Can change max_length
print(summarizer(ARTICLE, max_length=425, min_length=30, do_sample=False))

