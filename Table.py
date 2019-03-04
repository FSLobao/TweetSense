from os import chdir
import pandas as pd
import numpy as np
import io

# Enviroment settings
ProjectPath = "D:/Google_Drive/Master/Dgp/DGP_Proj_Code"

# Disable column truncating
pd.set_option('display.max_colwidth', -1)

# set read path
chdir(ProjectPath)

# read dataframes
dfTweetCount = pd.read_pickle("./DataStore/TweetCount.pkl")
dfTopRetweet = pd.read_pickle("./DataStore/TopRetweet.pkl")
dfTopUser = pd.read_pickle("./DataStore/TopUser.pkl")
dfTopPop = pd.read_pickle("./DataStore/TopPop.pkl")

# create table strings
TableTweetCount = dfTweetCount.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">') # use bootstrap styling
TableTopRetweet = dfTopRetweet.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">') # use bootstrap styling
TableTopUser = dfTopUser.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">') # use bootstrap styling
TableTopPop = dfTopPop.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">') # use bootstrap styling

#create HTML report as a string
html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="./css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>Twitter Analist </h1>
        <h2>TWEET TREND: Ammount of tweet in a given time period and label, expressend in total and per sentiment analisis value</h2>
        ''' + TableTweetCount + '''
        <h2>TOP TWEETS - Top tweets defined by the ammount of retweet in a given time period and label</h2>
        ''' + TableTopRetweet + '''
        <h2>TOP TWITTERS - Top users as defined by the ammount of tweets in a given time period and label</h2>
        ''' + TableTopUser + '''
        <h2>TOP INFLUENCERS - Top users as defined by the ammount of followers in a given time period and label</h2>
        ''' + TableTopPop + '''
    </body>
</html>'''

# record the report
with open('./Report/TableReport.html', mode='w', encoding='UTF-8') as FileAnchor: FileAnchor.write(html_string)
#FileAnchor.close()

# Indicate end
print('\nTable Report Created')
