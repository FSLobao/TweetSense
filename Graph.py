from os import chdir
import pandas as pd
import numpy as np
import io

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, plot
from plotly import tools

# Enviroment settings
QueryLabels = ['emt','metro','valenbici','NO MATCH'] #this should be the same used on the dataframe and presented in alphabetic order
Timeslots = [0,12,48,96,192] #hours in each time slot
TopNumber = 5 # length of the top list. e.g. = 5  will take the five highst values
ProjectPath = "D:/Google_Drive/Master/Dgp/DGP_Proj_Code"
sentiments_label = ['Negatividad Muy Alta', 'Negatividad Alta', 'Negatividad Mediana', 'Negatividad Baja', 'Sin Negatividad', 'Sin Positividad', 'Positividad Baja', 'Positividad Mediana', 'Positividad Elevada', 'Positividad Muy Elevada']
scolors = ['rgba(191, 63, 63, 1)', 'rgba(191, 63, 63, 0.8)', 'rgba(191, 63, 63, 0.6)', 'rgba(191, 63, 63, 0.4)', 'rgba(191, 63, 63, 0.2)', 'rgba(63, 63, 191, 0.2)', 'rgba(63, 63, 191, 0.4)', 'rgba(63, 63, 191, 0.6)', 'rgba(63, 63, 191, 0.8)', 'rgba(63, 63, 191, 1']

# Disable column truncating
pd.set_option('display.max_colwidth', -1)

# set read path
chdir(ProjectPath+'/Report')

# read dataframes
dfTweetCount = pd.read_pickle("../DataStore/TweetCount.pkl")
dfTopRetweet = pd.read_pickle("../DataStore/TopRetweet.pkl")
dfTopUser = pd.read_pickle("../DataStore/TopUser.pkl")
dfTopPop = pd.read_pickle("../DataStore/TopPop.pkl")

###################
# TOP TREND GRAPH #
###################

#initialize lists
xdata = ['']*len(Timeslots)
data = [0]*len(sentiments_label)
sentiments = list(range(-5,0))+list(range(1,6))

#set layout for bar graph
layout = go.Layout(
    barmode='stack',
    title=''
)

#set x axix labels
for i in range(len(QueryLabels)-1):
    # set the title reference to the label 
    layout['title']=(QueryLabels[i].upper())+': Cantidad de Tweets por Sentimento Positivo y Negativo'

    # select data for each label in turn
    dfSel = dfTweetCount[(dfTweetCount['QueryLabel'] == QueryLabels[i])]

    dfSel.reset_index(drop = True, inplace = True)

    # sweet time stamps to create x axis label
    for j in range(len(Timeslots)):
        xdata[j] =  'de: '+dfSel.loc[j,'TimeStop'].strftime('%d/%m %H')+"h a "+dfSel.loc[i,'TimeStart'].strftime('%d/%m %H'+"h")

    # cicle through list to set values
    for j in range(len(sentiments)):
        ydata = (100*dfSel[sentiments[j]]/(2*dfSel['TweetCount'])).fillna(0).round(0)
        datalabel = ['']*len(ydata)
        for k in range(len(ydata)):
            datalabel[k] = str(ydata[k])+"%: "+str(dfSel[sentiments[j]][k])+" Tweets"
        data[j] = go.Bar(
            x=xdata,
            y=ydata,
            name = sentiments_label[j],
            text= datalabel,
            marker=dict(color=scolors[j]))


    plot(go.Figure(data=data, layout=layout), filename=QueryLabels[i]+' TWEET TREND plot.html')

###################
# TOP TWEET GRAPH #
###################

#set layout for bar graph
labelxaxis = go.XAxis(
    range=[0, 6],
    showgrid=True,
    ticks="", 
    showticklabels=True,
    ticktext=['']+[str(i) for i in list(range(1,6))]+[''],
    tickvals=list(range(7))
)
labelyaxis = go.YAxis(
    autorange='reversed',
    range=[-6, 0],
    showgrid=True,
    ticks="", 
    showticklabels=True,
    ticktext=['']+[str(i) for i in list(range(-5,0))]+[''],
    tickvals=list(range(-6,1))
)
layout = go.Layout(
    title='',
    xaxis=labelxaxis,
    yaxis=labelyaxis,
)

# define references for traces
traces = dfTopRetweet.TimeStart.unique()
areamin = dfTopRetweet['Retweet'].min()
areamax = (dfTopRetweet['Retweet'].max())-areamin
sizeref=100
xdata = ['']*len(Timeslots)
data = [0]*len(traces)
sentiments = list(range(-5,0))+list(range(1,6))

# for each label produce a graph
for i in range(len(QueryLabels)-1):
    # set the title reference to the label 
    layout['title']=(QueryLabels[i].upper())+': Tweets con más Retweets'

    # for each timeslot produce a trace in a graph
    for j in range(len(traces)):
        
        # select the data for each trace. Use the first rows of the TopRetweet to reconstruct a timestamp reference for each trace
        dfSel = dfTopRetweet[(dfTopRetweet['QueryLabel'] == QueryLabels[i]) & (dfTopRetweet['TimeStart'] == traces[j]) ]

        #reset index
        dfSel.reset_index(drop = True, inplace = True)

        data[j] = go.Scatter(
            x=dfSel['Positive Sentiment'],
            y=dfSel['Negative Sentiment'],
            mode='markers',
            name = str(Timeslots[j])+' horas',
            text= dfSel['TweetText'],
            marker=dict(
                #sizemode='area',
                sizemin = 5,
                #sizeref=sizeref,
                size=((dfSel['Retweet'].tolist()-areamin)/areamax)*150,
                #line=dict(width=2)
                ))
        
    plot(go.Figure(data=data, layout=layout), filename=QueryLabels[i]+' TOP TWEET plot.html')


###################
# TOP TWITTERS GRAPH #
###################

#set layout for bar graph
labelxaxis = go.XAxis(
    range=[0, 6],
    showgrid=True,
    ticks="", 
    showticklabels=True,
    ticktext=['']+[str(i) for i in list(range(1,6))]+[''],
    tickvals=list(range(7))
)
labelyaxis = go.YAxis(
    autorange='reversed',
    range=[-6, 0],
    showgrid=True,
    ticks="", 
    showticklabels=True,
    ticktext=['']+[str(i) for i in list(range(-5,0))]+[''],
    tickvals=list(range(-6,1))
)
layout = go.Layout(
    title='',
    xaxis=labelxaxis,
    yaxis=labelyaxis,
)

# define references for traces
traces = dfTopUser.TimeStart.unique()
areamin = dfTopUser['Amount'].min()
areamax = (dfTopUser['Amount'].max())-areamin
sizeref=100
xdata = ['']*len(Timeslots)
data = [0]*len(traces)
sentiments = list(range(-5,0))+list(range(1,6))

# for each label produce a graph
for i in range(len(QueryLabels)-1):
    # set the title reference to the label 
    layout['title']=(QueryLabels[i].upper())+': Twitters con más Tweets'

    # for each timeslot produce a trace in a graph 
    for j in range(len(traces)):
        
        # select the data for each trace. Use the first rows of the TopRetweet to reconstruct a timestamp reference for each trace
        dfSel = dfTopUser[(dfTopUser['QueryLabel'] == QueryLabels[i]) & (dfTopUser['TimeStart'] == traces[j]) ]

        #reset index
        dfSel.reset_index(drop = True, inplace = True)

        data[j] = go.Scatter(
            x=dfSel['Median Positive Sentiment'],
            y=dfSel['Median Negative Sentiment'],
            mode='markers',
            name = str(Timeslots[j])+' horas',
            text= dfSel['UserID'],
            marker=dict(
                #sizemode='area',
                sizemin = 5,
                #sizeref=sizeref,
                size=((dfSel['Amount'].tolist()-areamin)/areamax)*150,
                #line=dict(width=2)
                ))
        
    plot(go.Figure(data=data, layout=layout), filename=QueryLabels[i]+' TOP User plot.html')

    
###################
# TOP INFLUENCERS GRAPH #
###################
#set layout for radar graph
layout = go.Layout(
    title='',
    polar = dict(
        radialaxis = dict(
            visible = True,
            range = [0, 6]
        )
    )
)

# define references for traces
traces = dfTopPop.TimeStart.unique()

# for each label produce a graph
for i in range(len(QueryLabels)-1):
    # for each timeslot produce a trace in a graph 
    for j in range(len(traces)):
        
        # select the data for each trace. Use the first rows of the TopRetweet to reconstruct a timestamp reference for each trace
        dfSel = dfTopUser[(dfTopPop['QueryLabel'] == QueryLabels[i]) & (dfTopPop['TimeStart'] == traces[j]) ]

        #reset index
        dfSel.reset_index(drop = True, inplace = True)

        #set layout for radar graph
        layout['title']=(QueryLabels[i].upper())+': Twitters con más seguidores en las ultimas '+str(Timeslots[j])+' horas'
        
        data = [
            go.Scatterpolar(
                r = dfSel['Median Positive Sentiment'],
                theta = dfSel['UserID'],
                fill = 'toself',
                name = 'Positive Sentiment'),
            go.Scatterpolar(
                r = (dfSel['Median Negative Sentiment'])*-1,
                theta = dfSel['UserID'],
                fill = 'toself',
                name = 'Negative Sentiment')
        ]
        
        plot(go.Figure(data=data, layout=layout), filename=QueryLabels[i]+' TOP Pop plot - '+str(Timeslots[j])+'.html')


# https://stackoverflow.com/questions/36262748/python-save-plotly-plot-to-local-file-and-insert-into-html
# fig = plot(go.Figure(data=data, layout=layout), include_plotlyjs=True, output_type='div')

print('\nGraphics Created')
