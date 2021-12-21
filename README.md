# Twitter-Trend-Nature
To check the nature(ie. sentiment) of current trends on twitter 

## Setup
1) Download the dataset from the url:
    https://drive.google.com/file/d/1_Wxgkfynms67F_zuA1hgXwgf-lZ1hpkW/view?usp=sharing
2) Install requirements.txt
    pip install -r requirements.txt
3) Get Twitter API Access via. twitter developer account (skippable)

## To build sentiment model
1) Download Dataset add to pk folder
2) Run jupyter notebook /pk/model.ipynb

## To run UI Dashboard
1) Run the following command,
    python app.py

## To run backend server
1) Run Django Server
    python manage.py runserver

## Available API's
### 1) To Fetch Today's Trends
Method: GET
URL: {localhost}/getTrends/
### 2) To Fetch Tweets by Keyword
Method: GET
URL: {loacalhost}/getTweets/{keyword}/
