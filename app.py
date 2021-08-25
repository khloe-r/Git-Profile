import requests
import json
from flask import Flask, render_template

app = Flask(__name__)

# UserURL = requests.get("https://api.github.com/users/khloe-r")
# user_result = UserURL.json()
# languages = {}

# print()

# if (True):
#     print('username', user_result['login'])
#     print('img', user_result['avatar_url'])
#     print('name', user_result['name'])
#     print()

#     ReposURL = requests.get(user_result['repos_url'])
#     repo_result = ReposURL.json()
#     for repo in repo_result:
#         print('name', repo['name'])
#         LanguageURL = requests.get(repo['languages_url'])
#         language_result = LanguageURL.json()
#         for lang in language_result:
#             if lang in languages:
#                 languages[lang] += language_result[lang]
#             else:
#                 languages[lang] = language_result[lang]

# print(languages)
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')


