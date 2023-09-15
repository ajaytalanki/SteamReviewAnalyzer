# SteamScraper
## Summary
This program uses the Steamworks API to retrieve a list of reviews of a steam game given the app ID. These reviews are run through the RoBERTa natural language processing model
for sentiment analysis. The model produces sentiment scores for each review, and the scores are averaged and plotted in a distribution for analysis. 

## Steam Web API Key
You will first need a Steamworks Web API key to retrieve the user reviews. This can be done by following the steps on the [Authentication using Web API Keys](https://partner.steamgames.com/doc/webapi_overview/auth) website.

## Steam App ID
In order to analyze the reviews of a given game, you must supply the App ID of the steam game. This can be found using a simple google search.

## Sentiment Scores
The RoBERTa model produces a sentiment score array for each review following the format = [negative score, neutral score, positive score].

**Positive Score:**
Definition: The positive score represents the degree or intensity of positive sentiment expressed in the text. It quantifies how positive or favorable the text is.  
Range: Typically, positive scores can be represented on a numerical scale. A higher positive score indicates a more positive sentiment, with the range being 0-1.

Neutral Score:

Definition: The neutral score indicates that the text does not express a strong positive or negative sentiment. It represents a lack of strong emotion or a balanced mix of positive and negative sentiments.
Range: Neutral scores often fall close to 0 on a numerical scale. In some systems, a neutral score might be considered within a narrow range around 0, such as between -0.1 and 0.1.
Example: A neutral score of 0.05 suggests that the text is slightly positive but leans mostly towards neutrality.
Negative Score:

Definition: The negative score represents the degree or intensity of negative sentiment expressed in the text. It quantifies how negative or unfavorable the text is.
Range: Like the positive score, negative scores are typically represented on a numerical scale. A higher negative score indicates a more negative sentiment, with the minimum score usually being -1 (or -100%) to represent very negative sentiment.
Example: If a text has a negative score of -0.7, it suggests that the text contains a significant amount of negative sentiment.
