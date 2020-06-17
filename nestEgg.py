
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go  
import numpy as np
import pandas as pd
import random 
import time 

app = dash.Dash()

#create data for age dropdowns 
ageList = list(np.linspace(65,110,46))
ageOptions = []
for num in ageList:
    ageOptions.append({'label':str(int(num)),'value':int(num)})

#load historical returns 
df =  pd.read_csv('sp-500-historical-annual-returns.csv')
returns = list(df['return'])


#create data for default values for lifetime distribution
lives = list(np.random.triangular(75,80,95,3000))
for ind, value in enumerate(lives):
    lives[ind] = int(value)

data =[go.Histogram(x=lives)]
layout = go.Layout(title='Distribution of Lifetimes')
fig = go.Figure(data=data, layout=layout)

#create data for default values for savings at end of life
savings = 1000000
annualSpend  = 50000
savingsLeftover = []

for life in lives:
    retirementYears = life-65
    randStart = random.randint(0, len(returns))
    individualSavings = savings
    individualSpend = annualSpend
    for year in range(retirementYears):
        individualSavings -=individualSpend
        selector = (year+randStart)%len(returns)
        growth = returns[selector]
        individualSavings = (individualSavings*growth)+individualSavings
    savingsLeftover.append(individualSavings)
    positives = []

    for sav in savingsLeftover:
        if sav>0:
            positives.append(1)
        else:
            positives.append(0)
    
    poz = sum(positives)/len(positives)
    neg = 1- poz
    labels = ['Positive Savings', 'Negative Savings']
    values = [poz, neg]

layoutPie =go.Layout(title='Savings from Each Lifetime')
figPie= go.Figure(data=[go.Pie(labels=labels, values=values)], layout=layoutPie)


saveLayout=go.Layout(title='Savings from Each Lifetime')
figSave = go.Figure(data=[go.Histogram(x=savingsLeftover)], layout=saveLayout)





# print(ageOptions)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H5('Min Age'),
            dcc.Dropdown(id="lowAge", options=ageOptions, value=75), 
            html.H5('Most Likely Age'),
            dcc.Dropdown(id="modeAge", options=ageOptions, value=80), 
            html.H5('Max Age'),
            dcc.Dropdown(id="highAge", options=ageOptions, value=95), 
            html.H5('Savings'),
            dcc.Input(id='savings', type='number', placeholder = 1000000),
            html.H5('Annual Spend'), 
            dcc.Input(id='spend', type='number', placeholder = 50000),
            html.Button('Submit', id='submitButt', n_clicks=0),

    ], style={'width': '25%', 'height': '450px','float':'left'}),
    html.Div([
        dcc.Graph(figure=fig, id="lifeGraph")
    ],style={'margin-left':'25%', 'height':'450px', 'width':'60%'})
    ],style={'margin':'auto', 'height':'450px', 'padding':'5px'}),
html.Div([
    dcc.Graph(figure =figPie, id='output_percentage', style={'float':'left','width':'25%'}),
        dcc.Graph(figure=figSave, id='saveGraph', style={'width':'75%','margin-left':'25%'})
    ], style = {'margin':'auto', 'height':'450px', 'padding':'5px'})

])

@app.callback(
    dash.dependencies.Output('lifeGraph', 'figure'), 
    [dash.dependencies.Input('submitButt', 'n_clicks')],
    [dash.dependencies.State('lowAge', 'value'),
    dash.dependencies.State('modeAge', 'value'),
    dash.dependencies.State('highAge', 'value')]
)

def update_lifetimes_dist(n_clicks, low, mode, high):
    lives = np.random.triangular(low, mode, high,3000)
    for ind, value in enumerate(lives):
        lives[ind] = int(value)

    data =[go.Histogram(x=lives)]
    layout = go.Layout(title='Distribution of Lifetimes')
    fig = go.Figure(data=data, layout=layout)
    return fig


@app.callback(
    dash.dependencies.Output('saveGraph', 'figure'), 
    [dash.dependencies.Input('submitButt', 'n_clicks')],
    [dash.dependencies.State('savings', 'value'),
    dash.dependencies.State('spend', 'value')]
)

def update_savings_dist(n_clicks, savings, spend):
    savingsLeftover=[]
    for life in lives:
        retirementYears = life-65
        randStart = random.randint(0, len(returns))
        individualSavings = savings
        individualSpend = annualSpend
        for year in range(retirementYears):
            individualSavings = individualSavings - individualSpend
            selector = (year+randStart)%len(returns)
            growth = returns[selector]
            individualSavings = (individualSavings*growth)+individualSavings
        savingsLeftover.append(individualSavings)

    positives = []

    for sav in savingsLeftover:
        if sav>0:
            positives.append(1)
        else:
            positives.append(0)


    saveLayout=go.Layout(title='Savings from Each Lifetime')
    figSave = go.Figure(data=[go.Histogram(x=savingsLeftover, color=positives)], layout=saveLayout)

    return figSave


@app.callback(
    dash.dependencies.Output('output_percentage', 'figure'), 
    [dash.dependencies.Input('submitButt', 'n_clicks')],
    [dash.dependencies.State('savings', 'value'),
    dash.dependencies.State('spend', 'value')]
)

def output_percentage(n_clicks, savings, spend):
    savingsLeftover=[]
    for life in lives:
        retirementYears = life-65
        randStart = random.randint(0, len(returns))
        individualSavings = savings
        individualSpend = annualSpend
        for year in range(retirementYears):
            individualSavings = individualSavings - individualSpend
            selector = (year+randStart)%len(returns)
            growth = returns[selector]
            individualSavings = (individualSavings*growth)+individualSavings
        savingsLeftover.append(individualSavings)
    positives = []

    for sav in savingsLeftover:
        if sav>0:
            positives.append(1)
        else:
            positives.append(0)
    
    poz = sum(positives)/len(positives)
    neg = 1- poz
    labels = ['Positive Savings', 'Negative Savings']
    values = [poz, neg]

    layoutPie =go.Layout(title='Savings from Each Lifetime')
    figPie= go.Figure(data=[go.Pie(labels=labels, values=values)], layout=layoutPie)

    return figPie


app.run_server(debug=False, use_reloader=False)