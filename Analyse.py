from os import chdir
import pandas as pd
import numpy as np

# https://jeffdelaney.me/blog/useful-snippets-in-pandas/
# https://www.datacamp.com/community/tutorials/pandas-multi-index
# https://jakevdp.github.io/PythonDataScienceHandbook/03.05-hierarchical-indexing.html
# https://www.somebits.com/~nelson/pandas-multiindex-slice-demo.html


# Define labels to search, last element is to be used when none of the previous is used
QueryLabels = ['emt','metro','valenbici','NO MATCH'] #this should be the same used on the dataframe and presented in alphabetic order
Timeslots = [0,12,48,96,192] #hours in each time slot
TopNumber = 5 # length of the top list. e.g. = 5  will take the five highst values
ProjectPath = "D:/Google_Drive/Master/Dgp/DGP_Proj_Code"

# main program

# give line space for later progress indication
print('')

# set read path
chdir(ProjectPath+"/DataStore")

# load tweeter dataframe
df = pd.read_pickle("AllTweet.pkl")

# order the dataframe in respect to time
df.sort_values(by=['Date'],ascending=False,inplace=True)

# set initial values of the time rages to maximum an minimum timestamps in the dataframe (time boundries)
# since the first and last are included, all comparisons should include the boundries. These are not overlaping
TimeStart = [max(df['Date'])]*len(Timeslots)
TimeStop = [min(df['Date'])]*len(Timeslots)

# set time ranges as start and stop timestamps as lists based on the defined timeslots, except first start and last stop, that are kept with the boundry limits of the data
for i in range(len(Timeslots)-1):
    TimeStart[i+1] = TimeStart[0]-pd.DateOffset(hours=Timeslots[i+1])
    TimeStop[i] = TimeStart[0]-pd.DateOffset(hours=Timeslots[i+1])+pd.DateOffset(seconds=1)

# counter just to avoid repetition on the next operations
i = (len(QueryLabels)-1)*len(Timeslots)

# create a dataframe (first tree columns) to store counts (total and per sentiment) for time and label slices
dfTime = pd.DataFrame(data={
 'QueryLabel': [QueryLabels[-1]]*i, # temporary asigment just for the creation of the object
 'TimeStart': TimeStart*(len(QueryLabels)-1),
 'TimeStop' : TimeStop*(len(QueryLabels)-1)})

# sweep dataframe and set query lables correctly
for i in range((len(QueryLabels)-1)):
    for j in range(len(Timeslots)):
        # compute the row index
        k = (i*len(Timeslots))+j

        # correct the QueryLabel for de dfTime
        dfTime.at[k,'QueryLabel'] = QueryLabels[i]


# create a dataframe (first four columns) to store to tweet list for time and label slices
dfTopRetweet = dfTime.assign(Top=1)
for i in range(2,TopNumber+1):
    dfTopRetweet = dfTopRetweet.append(dfTime.assign(Top=i), ignore_index=True)

# sort dataframe based on retweet
dfTopRetweet = dfTopRetweet.sort_values(by=['QueryLabel','TimeStart','Top'], ascending=[True,False,True])
dfTopRetweet = dfTopRetweet.reset_index(drop=True)

# Copy the basic framework to be used on other top lists
dfTopUser = dfTopRetweet.copy()
dfTopPop = dfTopRetweet.copy()

# sweep dataframe and set values
for i in range((len(QueryLabels)-1)):
    for j in range(len(Timeslots)):
        # compute the row index
        k = (i*len(Timeslots))+j

        # print processing indicator message
        print("\r"+str(round(100*(k/ (( (len(QueryLabels)-2)*len(Timeslots) ) + (len(Timeslots)-1) ) )))+"% done - QueryLable: "+QueryLabels[i]+", TimeSlot: "+str(Timeslots[j])+"         ", end='')

        # select de databased on time and label, creating a sliced dataframe
        dfSel = df[(df['Date'] <= dfTime.loc[k,'TimeStart']) & (df['Date'] >= dfTime.loc[k,'TimeStop']) & (df['QueryLabel'] == QueryLabels[i]) ]
        
        # TWEET TREND -  analyse slice to select ammount of tweet in the given time period and label with specific sentiment analisis value
        # analyse de slice, counting tweets and tweets per each sentiment level
        # sentiment levels varies from -5 to -1 and 1 to 5, by sentistrength definitions 
        dfTime.at[k,'TweetCount'] = len(dfSel)
        for l in range(-5,0): 
            dfTime.at[k,l] = len(dfSel[(dfSel['NegativeS']==l)])
        for l in range(1,6):
            dfTime.at[k,l] = len(dfSel[(dfSel['PositiveS']==l)])

        # TOP TWEETS - analyse slice to select top tweets defined by the ammount of retweet in the given time period and label
        # sort dataframe based on retweet
        dfTopFive = dfSel.sort_values(by='Retweets', ascending=False).head(TopNumber)

        # proceed only if dataframe is not empty (is there any tweet in the given time period and label)
        if not dfTopFive.empty:
            # analyse de slice, finding top tweets based on amount of retweets per period of time and label
            # must loop through all the elments in the dfTopRetweet list such as to remove NaN values with the if and try strategies
            # discosiders tweets that were not retweeted and periodes where there are no tweets 
            for l in range(TopNumber):
                # compute the row index
                m = k*TopNumber+l

                # Continue If the index is within the size of de dfTopFive dataframe, for the given time period and label
                # Might be less tweets than the ammount defined in "TopNumber"
                if l < len(dfTopFive):
                    # Only stores data if there are retweets for the given time period and label
                    if dfTopFive.iloc[l]['Retweets'] > 0:
                        dfTopRetweet.at[m,'Retweet'] = dfTopFive.iloc[l]['Retweets']
                        dfTopRetweet.at[m,'TweetID'] = dfTopFive.iloc[l]['Tweet ID']
                        dfTopRetweet.at[m,'TweetText'] = dfTopFive.iloc[l]['Tweet Text']
                        dfTopRetweet.at[m,'Positive Sentiment'] = dfTopFive.iloc[l]['PositiveS']
                        dfTopRetweet.at[m,'Negative Sentiment'] = dfTopFive.iloc[l]['NegativeS']
                    # Else remove the row with retweet=0 for the given time period and label
                    else:
                        dfTopRetweet=dfTopRetweet.drop(m)
                # If the amount of tweets is less than the one defined in "TopNumber"
                else:
                    # Remove the row for the given time period and label where there are no tweets
                    dfTopRetweet=dfTopRetweet.drop(m)
        # If there is no tweets within the given time period and label, 
        else:
            # remove all corresponding rows with no tweets
            dfTopRetweet=dfTopRetweet.drop(list(range((k*TopNumber),((k+1)*TopNumber))))

        # TOP TWITTERS - analyse slice to select top users as defined by the ammount of tweets for the given time period and label
        dfTopFive = dfSel.groupby('Screen Name').count().sort_values(by='Date', ascending=False).head(TopNumber)

        #reset row indexes created to a column 
        dfTopFive.reset_index(level=0,inplace=True)

        #proceed only if dataframe is not empty (is there any tweet in the given time period and label)
        if not dfTopFive.empty:
            # analyse de slice, finding top tweets based on amount of retweets per period of time and label
            # must loop through all the elments in the dfTopRetweet list such as to remove NaN values with the if and try strategies
            # discosiders tweets that were not retweeted and periodes where there are no tweets 
            for l in range(TopNumber):
                # compute the row index
                m = k*TopNumber+l

                # Continue If the index is within the size of de dfTopFive dataframe, for the given time period and label
                # Might be less tweets than the ammount defined in "TopNumber"
                if l < len(dfTopFive):
                    # Only stores data if there are amount for the given user time period and label is greater than zero
                    if dfTopFive.iloc[l]['Date'] > 0:
                        dfTopUser.at[m,'Amount'] = dfTopFive.iloc[l]['Date']
                        dfTopUser.at[m,'UserID'] = dfTopFive.iloc[l]['Screen Name']
                        dfTopUser.at[m,'Median Positive Sentiment'] = dfSel[ (dfSel['Screen Name'] == dfTopFive.iloc[l]['Screen Name']) ]['PositiveS'].median()
                        dfTopUser.at[m,'Max Positive Sentiment'] = dfSel[ (dfSel['Screen Name'] == dfTopFive.iloc[l]['Screen Name']) ]['PositiveS'].max()
                        dfTopUser.at[m,'Median Negative Sentiment'] = dfSel[ (dfSel['Screen Name'] == dfTopFive.iloc[l]['Screen Name']) ]['NegativeS'].median()
                        dfTopUser.at[m,'Max Negative Sentiment'] = dfSel[ (dfSel['Screen Name'] == dfTopFive.iloc[l]['Screen Name']) ]['NegativeS'].min()
                    # Else remove the row with retweet=0 for the given time period and label
                    else:
                        dfTopUser=dfTopUser.drop(m)
                # If the amount of tweets is less than the one defined in "TopNumber"
                else:
                    # Remove the row for the given time period and label where there are no tweets
                    dfTopUser=dfTopUser.drop(m)
        # If there is no tweets within the given time period and label, 
        else:
            # remove all corresponding rows with no tweets
            dfTopUser=dfTopUser.drop(list(range((k*TopNumber),((k+1)*TopNumber))))

        # TOP FOLLOWED - Analyse slice to select top users as defined by the ammount of followers for the given time period and label
        dfTopFive = dfSel.groupby('Screen Name').max().sort_values(by='Followers', ascending=False).head(TopNumber)

        #reset row indexes created to a column 
        dfTopFive.reset_index(level=0,inplace=True)

        #proceed only if dataframe is not empty (is there any tweet in the given time period and label)
        if not dfTopFive.empty:
            # analyse de slice, finding top tweets based on amount of retweets per period of time and label
            # must loop through all the elments in the dfTopRetweet list such as to remove NaN values with the if and try strategies
            # discosiders tweets that were not retweeted and periodes where there are no tweets 
            for l in range(TopNumber):
                # compute the row index
                m = k*TopNumber+l

                # Continue If the index is within the size of de dfTopFive dataframe, for the given time period and label
                # Might be less tweets than the ammount defined in "TopNumber"
                if l < len(dfTopFive):
                    dfTopPop.at[m,'Followers'] = dfTopFive.iloc[l]['Followers']
                    dfTopPop.at[m,'UserID'] = dfTopFive.iloc[l]['Screen Name']
                    dfTopPop.at[m,'Median Positive Sentiment'] = dfSel[ (dfSel['Screen Name'] == dfTopFive.iloc[l]['Screen Name']) ]['PositiveS'].median()
                    dfTopPop.at[m,'Max Positive Sentiment'] = dfSel[ (dfSel['Screen Name'] == dfTopFive.iloc[l]['Screen Name']) ]['PositiveS'].max()
                    dfTopPop.at[m,'Median Negative Sentiment'] = dfSel[ (dfSel['Screen Name'] == dfTopFive.iloc[l]['Screen Name']) ]['NegativeS'].median()
                    dfTopPop.at[m,'Max Negative Sentiment'] = dfSel[ (dfSel['Screen Name'] == dfTopFive.iloc[l]['Screen Name']) ]['NegativeS'].min()
                # If the amount of tweets is less than the one defined in "TopNumber"
                else:
                    # Remove the row for the given time period and label where there are no tweets
                    dfTopPop=dfTopPop.drop(m)
        # If there is no tweets within the given time period and label, 
        else:
            # remove all corresponding rows with no tweets
            dfTopPop=dfTopPop.drop(list(range((k*TopNumber),((k+1)*TopNumber))))


# store data in pandas format
dfTime.to_pickle("TweetCount.pkl")
dfTopRetweet.to_pickle("TopRetweet.pkl")
dfTopUser.to_pickle("TopUser.pkl")
dfTopPop.to_pickle("TopPop.pkl")

# store data in csv format for reuse
dfTime.to_csv("TweetCount.csv", encoding='utf-8')
dfTopRetweet.to_csv("TopRetweet.csv", encoding='utf-8')
dfTopUser.to_csv("TopUser.csv", encoding='utf-8')
dfTopPop.to_csv("TopPop.csv", encoding='utf-8')

print('\rProcessing completed                                                  ')


# print ("dfTime:       "+str(list(dfTime))+"\ndfTopRetweet: "+str(list(dfTopRetweet))+"\ndfTopUser:    "+str(list(dfTopUser))+"\ndfTopPop:     "+str(list(dfTopPop)))
# print ("\n\n#dfTime:\n"+str(dfTime.head(2))+"\n\n#dfTopRetweet:\n"+str(dfTopRetweet.head(2))+"\n\n#dfTopUser:\n"+str(dfTopUser.head(2))+"\n\n#dfTopPop:\n"+str(dfTopPop.head(2)))

# print ("dfSel:       "+str(list(dfSel))+"\ndfTopFive: "+str(list(dfTopFive)))
# print ("\n\n#dfSel:\n"+str(dfSel.head(2))+"\n\n#dfTopFive:\n"+str(dfTopFive.head(2)))