import requests
from flask import Flask, render_template,request
from datetime import datetime
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

app = Flask(__name__)

# Languages Used Graph
def create_pie(langs):

    N = 5
    x = langs.keys() #np.linspace(0, 1, N)
    y = langs.values() #np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Pie(
            labels=df['x'], # assign x as the dataframe column 'x'
            values=df['y'],
            domain={
                'x': [0.90,0.90],
                'y': [0,1]
            }
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

# Stars per Language Graph
def create_plot(stars):

    N = 5
    x = stars.keys() #np.linspace(0, 1, N)
    y = stars.values() #np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods = ['POST', 'GET'])
def results():
    if request.method == 'GET':
        return render_template('error.html', error="The URL /results cannot be accessed directly. Try going to '/form' to submit form first!")
    if request.method == 'POST':
        form_data = request.form.to_dict()
        username = form_data['username_value']
        UserURL = requests.get("https://api.github.com/users/%s" % username) 
        user_result = UserURL.json()
        if 'message' not in user_result:
            languages = {}
            stars = {}
            repo_dates = []
            repos = []
            date = datetime.strptime(user_result['created_at'][0:10], '%Y-%m-%d')
            formatted_date = date.strftime("%B %d, %Y")
            ReposURL = requests.get(user_result['repos_url'])
            repo_result = ReposURL.json()
            for repo in repo_result:
                repo_dates.append(repo['updated_at'][0:10] + " " + repo['updated_at'][11:19])
                LanguageURL = requests.get(repo['languages_url'])
                language_result = LanguageURL.json()
                for lang in language_result:
                    if lang != "message" and lang != "documentation_url":
                        if lang in languages:
                            languages[lang] += 1 #language_result[lang]
                            stars[lang] += int(repo['stargazers_count'])
                        else:
                            languages[lang] = 1 #language_result[lang]
                            stars[lang] = int(repo['stargazers_count'])

            sorted = list(repo_dates)
            sorted.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d %H:%M:%S'), reverse=True)
            for i in range(min(len(sorted), 4)):
                repo_data = repo_result[repo_dates.index(sorted[i])]
                repos.append({
                    'name': repo_data['name'],
                    'lang': repo_data['language'],
                    'descript': (repo_data['description'] if repo_data['description'] != "None" else ""),
                    'forks': repo_data['forks_count'],
                    'stars': repo_data['stargazers_count'],
                    'watchers': repo_data['watchers_count'],
                    'view': repo_data['html_url'],
                    'clone': repo_data['clone_url'],
                    'updated': datetime.strptime(repo_data['updated_at'][0:10], '%Y-%m-%d').strftime("%B %d, %Y")
                    })

            pie = create_pie(languages)
            bar = create_plot(stars)
            return render_template(
                'results.html',
                username=user_result['login'],
                img=user_result['avatar_url'],
                name=user_result['name'],
                bio=user_result['bio'],
                web=user_result['blog'],
                followers=user_result['followers'],
                following=user_result['following'],
                repos=user_result['public_repos'],
                date=formatted_date,
                plot=pie,
                bar=bar,
                dates=repos,
                sorted=sorted
                )
        else:
            if (user_result['message'][0:14] == 'API rate limit'):
                error = "API limit exceeded!"
            else:
                error = "User not found!"
            return render_template('error.html', error=error)


