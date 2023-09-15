# SteamScraper
## Summary
This program uses the Steamworks API to retrieve a list of reviews of a steam game given the app ID. These reviews are run through the RoBERTa natural language processing model
for sentiment analysis. The model produces sentiment scores for each review, and the scores are averaged and plotted in a distribution for analysis. 

## Steam Web API Key
You will first need a Steamworks Web API key to retrieve the user reviews. This can be done by following the steps on the [Authentication using Web API Keys](https://partner.steamgames.com/doc/webapi_overview/auth) website.

## Steam App ID
In order to analyze the reviews of a given game, you must supply the App ID of the steam game. This can be found using a simple google search.

## Sentiment Scores
The RoBERTa model produces a sentiment score array for each review following the format:  
\[negative score, neutral score, positive score\].  

**Negative Score:**
Definition: The negative score represents the degree or intensity of negative sentiment expressed in the text. It quantifies how negative or unfavorable the text is.  
Range: A higher negative score indicates a more negative sentiment, with the range being 0-1.  

**Neutral Score:**
Definition: The neutral score indicates that the text does not express a strong positive or negative sentiment. It represents a lack of strong emotion or a balanced mix of positive and negative sentiments.  
Range: A higher netural score indicates neither a negative or positive sentiment, with the range being 0-1.  

**Positive Score:**
Definition: The positive score represents the degree or intensity of positive sentiment expressed in the text. It quantifies how positive or favorable the text is.    
Range: A higher positive score indicates a more positive sentiment, with the range being 0-1.

## Visualization/Results
The program displays the distribution of frequencies for negative, neutral, and positive scores. The average of each score is also displayed.

## Limitations
Due to time and space constraints, the program only retrievs 500 reviews of the given steam game. These reviews may also not be representative of the population, as the reviews are retrieved by the API.  Lastly, reviews that are over 500 words are ignored, as this is intensive for the model.  




