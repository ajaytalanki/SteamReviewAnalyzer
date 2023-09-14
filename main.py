import requests
import urllib.parse
import sys
import re
import numpy as np
import threading
import matplotlib.pyplot as plt
import time 
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Makes encoded data displayable
sys.stdout.reconfigure(encoding='utf-8')

# Replace with Steamworks Web API key and APP ID of game
API_KEY = 'A6318394542B822701B68D53D6716E7B'
API_ID = '1716740'

MAX_REVIEWS = 400
review_list = []
num_reviews = 0
    
# determnes if the review contains majority irrelevant ascii_art
def is_ascii_art(text, threshold = 0.5):
    text = re.sub(r'\s', '', text)
    total_chars = len(text)
    if total_chars == 0:
        return False
    non_alphanumeric_chars = len(re.findall(r'[^a-zA-Z0-9]', text))
    percentage = (non_alphanumeric_chars / total_chars)
    return percentage > threshold

# determines if the review is a checklist, this makes is hard to analyze
def too_many_paragraphs(review, threshold = 5):
    copy = review
    paragraphs = copy.split('\n')
    return len(paragraphs) >= threshold

# determines if the review is too long for model to analyze
def too_many_words(review, threshold = 500):
     copy = review
     return len(copy.split()) > threshold
     
# Endpoint parameters for the Steamwork API
cursor = '*'
num_per_page = 100

start = time.time()

# retrieve valid reviews from steam 
while num_reviews < MAX_REVIEWS:

    # Setup Steamworks API Endpoint
    encoded_cursor = urllib.parse.quote(cursor, safe='')
    url = f'https://store.steampowered.com/appreviews/{API_ID}?json=1&cursor={encoded_cursor}&num_per_page={num_per_page}'
    response = requests.get(url)

    # Successful GET request
    if response.status_code == 200:

        json = response.json()

        # No reviews to analyze
        if json['query_summary']['num_reviews'] == 0:
            break

        # retreive the reviews if they are english and not ascii art
        reviews = json['reviews']

        # populates list of valid reviews
        for review in reviews:
            review_text = review['review']
            if not is_ascii_art(review_text):
                if not too_many_paragraphs(review_text):
                    if not too_many_words(review_text):
                        review_list.append(review_text)
                        num_reviews += 1

        # Update cursor for the next URL
        cursor = json['cursor']
    else:
        print(f"Failed to retrieve game reviews. Status code: {response.status_code}")
        break

if(len(review_list) == 0):
    print("NO REVIEWS TO ANALYZE")
    sys.exit()

print("TIME TAKEN DOWNLOADING REVIEWS: ", time.time() - start)
start = time.time()

# downloads trained roberta model for sentiment analysis
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

print("TIME TAKEN DOWNLOADING MODEL: ", time.time() - start)

# tokenize and analyize each review
def process_review(review):
    encoded_text = tokenizer(review, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return scores

# function to process reviews concurrently
def process_reviews_thread(reviews_batch, pbar):
    for review in reviews_batch:
        scores = process_review(review)
        sentiment_scores.append(scores)
        pbar.update(1)  

sentiment_scores = []

# Create and start threads for each batch
threads = []
batch_size = 10
review_batches = [review_list[i:i+batch_size] for i in range(0, len(review_list), batch_size)]

start = time.time()

with tqdm(total=len(review_list), desc="Processing Reviews") as pbar:
    for batch in review_batches:
        thread = threading.Thread(target=process_reviews_thread, args=(batch, pbar))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

print("TIME TAKEN TO ANALYZE REVIEWS: ", time.time() - start)

sentiment_scores = np.array(sentiment_scores)
negative_scores = sentiment_scores[:, 0]
neutral_scores = sentiment_scores[:, 1]
positive_scores = sentiment_scores[:, 2]

# calculate average scores 
avg_neg = sum(negative_scores)/len(negative_scores)
avg_neu = sum(neutral_scores)/len(neutral_scores)
avg_pos = sum(positive_scores)/len(positive_scores)

print("AVERAGE NEGATIVE: ", avg_neg)
print("AVERAGE NEUTRAL: ", avg_neu)
print("AVERAGE POSITIVE: ", avg_pos)

# plot histogram
plt.figure(figsize=(10, 8))
plt.hist(negative_scores, bins=10, alpha=0.7, edgecolor='black')
plt.hist(neutral_scores, bins=10, alpha=0.7, edgecolor='black')
plt.hist(positive_scores, bins=10, alpha=0.7, edgecolor='black')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.legend()
plt.title('Distribution of Sentiment Scores')
plt.show()