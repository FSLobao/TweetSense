# Sentstrength routines
import subprocess
import shlex
import os.path
import sys

# Define labels to search, last element is to be used when none of the previous is used
QueryLabels = ['emt','valenbici','metro','NO MATCH']
ProjectPath = "D:/Google_Drive/Master/Dgp/DGP_Proj_Code"

# the SentiStrength data folder and to make this code work. These are near the top of the code below. The results will be saved to the folder where the YouTube files are kept. Only use forward slashes /.
SentiStrengthLocation = "D:/Google_Drive/Master/Dgp/DGP_Proj_Code/Sentistrength/SentiStrengthCom.jar" #The location of SentiStrength on your computer
SentiStrengthLanguageFolder = "D:/Google_Drive/Master/Dgp/DGP_Proj_Code/Sentistrength/Spanish/" #The location of the unzipped SentiStrength data files on your computer
    
# The following code tests that the above three locations are correct. If you don't get an error message then this is fine.
if not os.path.isfile(SentiStrengthLocation):
    print("SentiStrength not found at: ", SentiStrengthLocation)
if not os.path.isdir(SentiStrengthLanguageFolder):
    print("SentiStrength data folder not found at: ", SentiStrengthLanguageFolder)

# compute group based on query
def QueryGroup (row):
    # enforce the use of the labes defined outside the function
    global QueryLabels

    # define pointer to lable vector
    i = 0
    limit = len(QueryLabels)-1
    
    # start testing until a matching label is found
    while row.find(QueryLabels[i])<0 and i<limit:
        i = i+1

    return QueryLabels[i]

#  The code below allows SentiStrength to be called and run on a single line of text.

def RateSentiment(sentiString):
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar '" + SentiStrengthLocation + "' stdin sentidata '" + SentiStrengthLanguageFolder + "'"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    try:
        b = bytes(sentiString.replace(" ","+"), 'utf-8') #Can't send string in Python 3, must send bytes
    except:
        print ('erro!')
    stdout_byte, stderr_text = p.communicate(b)
    stdout_text = stdout_byte.decode("utf-8")  #convert from byte to a string
    stdout_text = stdout_text.split("\t") # convert string to a list
    return list(map(int,stdout_text[0:2])) # return converting the itens in the list from string to int
# Sentistrength outputs 2 values, one for positive and other for negative sentiments.
# Positive sentiments varies between 1 (not positive) to 5 (very positive) 
# Negative sentiments varies between -1 (not negative) to -5 (very negative

# main program
from os import listdir
from os import chdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import shutil

# set read path
chdir(ProjectPath+"/InBox")

#list files with csv extension that are on path defined in TweetsLocation 
filenames = [ filename for filename in listdir(ProjectPath+"/InBox") if filename.endswith( "csv" ) ]

#load dataframe or create one.
try:
    AllTweet = pd.read_pickle("../DataStore/AllTweet.pkl")
    newdf = False
except:
    newdf = True

# give line space for later progress indication
print('')

#Loop through files
for filename in filenames:

    # read first line with query information    
    with open(filename, mode="r", encoding="utf-8") as f:
        first_line = f.readline()
    f.close()

    # extract the query information from first line.
    # query information must between doble quotes
    f = pd.Series(first_line)
    querydata = f.str.split('"').tolist()[0][1]

    # read remaning file content and store it as pandas DataFrame
    Tweet = pd.read_csv(filename, header=1)

    # remove duplicate and empty tweets
    Tweet.drop_duplicates(subset=['Tweet ID'], keep='last', inplace=True)
    Tweet = Tweet.dropna(subset=['Tweet Text'])

    # add query information
    Tweet = Tweet.assign(query=querydata)
    
    # create simplified query label based on the label list
    Tweet['QueryLabel'] = Tweet['query'].apply (QueryGroup)

    # convert datetime from text to datetime variable within the dataframe
    Tweet['Date'] = pd.to_datetime(Tweet['Date'],dayfirst=True)
    Tweet['User Since'] = pd.to_datetime(Tweet['User Since'],dayfirst=False)

    # add two columns to store sentiment
    # Alternative using apply. Test didn`t indicate in significative performance gain
    # May try to use sentistrength alternative to process csv files`
    # Tweet['Sentiment'] = Tweet['Tweet Text'].apply (RateSentiment)
    
    #add two columns to store sentiment
    Tweet = Tweet.assign(**{'Sentiment': np.nan, 'NegativeS': np.nan}) 

    #line index counter
    LineCounter = list(Tweet.index.values)

    #sweep all rows in dataframe
    for line in LineCounter:
        [Tweet.loc[line, 'PositiveS'],Tweet.loc[line, 'NegativeS']] = RateSentiment(Tweet.loc[line, 'Tweet Text'])
        if (5*round(100*(line/(LineCounter[-1]*5))))==round(100*(line/LineCounter[-1])):
             print("\r"+str(round(100*(line/LineCounter[-1])))+"% de "+filename, end='')

    # append dataframe if one already exists
    if newdf:
        AllTweet = Tweet
        newdf = False
    else:
        AllTweet = AllTweet.append(Tweet, ignore_index=True)
    
        # remove duplicate tweets
        Tweet.drop_duplicates(subset=['Tweet ID'], keep='first', inplace=True)

    #store dataframe
    AllTweet.to_pickle("../DataStore/AllTweet.pkl")
    
    #move file to "Done Box"
    shutil.move(filename, "../DoneBox/"+filename)

    print("\r- "+filename+" processed -")

