import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from webcrawler import crawl_google

# constants
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
TOKENIZER = AutoTokenizer.from_pretrained("ProsusAI/finbert")
MODEL = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(DEVICE)
LABELS = ["positive", "negative", "neutral"]

# calculate total news article sentiments
def calculate_sentiment(date):
    articles = crawl_google(date)
    print(date)
    print(articles)
    if(len(articles) == 0):
        return None, None
    
    tokens = TOKENIZER(articles, return_tensors="pt", padding=True).to(DEVICE)

    result = MODEL(tokens["input_ids"], attention_mask=tokens["attention_mask"])[
        "logits"
    ]
    result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
    probability = result[torch.argmax(result)]
    sentiment = LABELS[torch.argmax(result)]
    
    return probability, sentiment