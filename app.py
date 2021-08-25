import requests
from flask import Flask, render_template
from datetime import datetime
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

app = Flask(__name__)

def create_plot(langs):

    N = 5
    x = langs.keys() #np.linspace(0, 1, N)
    y = langs.values() #np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

UserURL = requests.get("https://api.github.com/users/khloe-r")
user_result = UserURL.json()
languages = {}
repos = []

# print()

# if (True):
#     print('username', user_result['login'])
#     print('img', user_result['avatar_url'])
#     print('name', user_result['name'])
#     print()

# print(languages)
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    # date = datetime.strptime(user_result['created_at'][0:10], '%Y-%m-%d')
    # formatted_date = date.strftime("%B %d, %Y")
    ReposURL = requests.get(user_result['repos_url'])
    repo_result = ReposURL.json()
    for repo in repo_result:
        # print('name', repo['name'])
        LanguageURL = requests.get(repo['languages_url'])
        language_result = LanguageURL.json()
        for lang in language_result:
            repos.append(repo['name'])
            if lang in languages:
                repos.append(lang)
                languages[lang] += 1 #language_result[lang]
            else:
                languages[lang] = 1 #language_result[lang]

    bar = create_plot(languages)
    return render_template(
        'results.html',
        # username=user_result['login'],
        # img=user_result['avatar_url'],
        # name=user_result['name'],
        # bio=user_result['bio'],
        # web=user_result['blog'],
        # followers=user_result['followers'],
        # following=user_result['following'],
        # repos=user_result['public_repos'],
        # date=formatted_date,
        plot=bar,
        langdict=repos
        )


