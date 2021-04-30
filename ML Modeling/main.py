import streamlit as st
import pandas as pd
import numpy as np
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

	    
def extractTweet(number, sname, api):
	posts = api.user_timeline(screen_name = sname, count = number, lang= "en", tweet_mode="extended")
	return posts

def createDataframe(posts):
	df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

	return df

def cleanTxt(text):
  text = re.sub(r'@[A-Za-z0-9]+', '', text)  # r tells expression is raw string
  text = re.sub(r'#', '', text) #remove # symbol
  text = re.sub(r'RT[\s]+','', text) #Removing retweet
  text = re.sub(r'https?:\/\/\S+','', text) #remove the hyperlink

  return text

def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
  return TextBlob(text).sentiment.polarity

def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'

st.title("Twitter Sentiment Analyis")
st.set_option('deprecation.showPyplotGlobalUse', False)
tweet_extract = st.sidebar.selectbox("Select Number of Tweets to be extracted",("100","200","300"))
tweet_name = st.sidebar.selectbox("Select Whoes Tweets to be extracted",("narendramodi","BillGates","stevejobsceo"))

consumerKey = 'YOUR_CONSUMER_KEY'
consumerSecret = 'YOUR_CONSUMER_SECRET'
accessToken = 'YOUR_ACCESS_TOKEN'
accessTokenSeceret = 'YOUR_ACCESS_TOKEN_SECRET'
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
authenticate.set_access_token(accessToken, accessTokenSeceret)
api = tweepy.API(authenticate, wait_on_rate_limit= True)

posts = extractTweet(tweet_extract,tweet_name,api)

df = createDataframe(posts)
df['Tweets'] = df['Tweets'].apply(cleanTxt) # ? check apply functions
#Create two columns
df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)
df['Analysis'] = df['Polarity'].apply(getAnalysis)

#Plot the Word Cloud

allWords = ' '.join([twts for twts in df['Tweets']])
wordCloud = WordCloud(width = 500, height=300, random_state = 21, max_font_size=119).generate(allWords)

plt.imshow(wordCloud, interpolation="bilinear")
plt.axis('off')
st.pyplot()
# Plot the polarity and subjectivity

plt.figure(figsize=(8,6))
for i in range(0, df.shape[0]):
  plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='Blue')

plt.title('Sentiment Analysis')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
st.pyplot()

#Show the value counts

df['Analysis'].value_counts()

#plot and visualize the counts
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind='bar')
st.pyplot()
