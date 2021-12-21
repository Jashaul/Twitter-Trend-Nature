import pickle
import re
from numpy import positive
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords
# nltk.download('wordnet')

emojis = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad', 
          ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
          ':-@': 'shocked', ':@': 'shocked',':-$': 'confused', ':\\': 'annoyed', 
          ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
          '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
          '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink', 
          ';-)': 'wink', 'O:-)': 'angel','O*-)': 'angel','(:-D': 'gossip', '=^.^=': 'cat'}

def preprocess(textdata):
    processedText = []
    
    # Create Lemmatizer and Stemmer.
    wordLemm = WordNetLemmatizer()
    
    for tweet in textdata:
        tweet = tweet.lower()
        
        # Replace all URls with 'URL'
        tweet = re.sub(r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)",' URL',tweet)
        # Replace all emojis.
        for emoji in emojis.keys():
            tweet = tweet.replace(emoji, "EMOJI" + emojis[emoji])        
        # Replace @USERNAME to 'USER'.
        tweet = re.sub('@[^\s]+',' USER', tweet)        
        # Replace all non alphabets.
        tweet = re.sub("[^a-zA-Z0-9]", " ", tweet)
        # Replace 3 or more consecutive letters by 2 letter.
        tweet = re.sub(r"(.)\1\1+", r"\1\1", tweet)

        tweetwords = ''
        for word in tweet.split():
            if len(word)>1:
                # Lemmatizing the word.
                word = wordLemm.lemmatize(word)
                tweetwords += (word+' ')
            
        processedText.append(tweetwords)
        
    return processedText

def load_models():
    
    # Load the vectoriser. 
    file = open('pk/vectoriser-ngram-(1,2).pickle', 'rb')
    vectoriser = pickle.load(file)
    file.close()
    # Load the LR Model.
    file = open('pk/Sentiment-LR.pickle', 'rb')
    LRmodel = pickle.load(file)
    file.close()
    
    return vectoriser, LRmodel

def predict(text):
    vectoriser, model = load_models()
    
    processed_text = preprocess(text.tolist())
    
    # Predict the sentiment
    textdata = vectoriser.transform(processed_text)
    sentiment = model.predict(textdata)
    
    # Make a list of text with sentiment.
    data = []
    for text, pred in zip(processed_text, sentiment):
        data.append((text,pred))
        
    # Convert the list into a Pandas DataFrame.
    df = pd.DataFrame(data, columns = ['text','sentiment'])
    df = df.replace([0,1], ["Negative","Positive"])
    pos_words = df.loc[df['sentiment'] == 'Positive']['text']
    pos_count = len(pos_words)
    pos_words = " ".join(pos_words)
    pos_words = pos_words.replace('USER', "")
    pos_words = pos_words.replace('URL', "")

    neg_words = df.loc[df['sentiment'] == 'Negative']['text']
    neg_count = len(neg_words)
    neg_words = " ".join(neg_words)
    neg_words = neg_words.replace('USER', "")
    neg_words = neg_words.replace('URL', "")
    return df['sentiment'], [pos_count, pos_words], [neg_count, neg_words]