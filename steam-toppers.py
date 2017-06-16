from flask import Flask
from flask_ask import Ask, statement, question, session

import bs4 as bs
import urllib.request

url = 'http://store.steampowered.com/search/?filter=topsellers'
source = urllib.request.urlopen(url)
soup = bs.BeautifulSoup(source, 'lxml')

app = Flask(__name__)
ask = Ask(app, '/steam-toppers')

def get_top_games(num_top_games=10):
    games = []
    for title in soup.findAll('span', class_='title'):
        games.append(title)

    return [title.text.strip() for title in soup.findAll('span', class_='title')][:num_top_games]

@ask.launch
def start_skill():
    return yes_intent()

@ask.intent('YesIntent')
def yes_intent():
    msg = "Here are the top games today: {}".format(stringify_titles(get_top_games()))
    return statement(msg)

@ask.intent('NoIntent')
def no_intent():
    bye_text = 'Alright, bye then!'
    return statement(bye_text)

def stringify_titles(titles):
    if not titles:
        response = "I'm sorry, I couldn't get the information from Steam"
    elif len(titles) == 1:
        response = str(titles[0])
    else:
        response = ', '.join(str(title) for title in titles[:-1])
        response += ', and ' + str(titles[-1])

    return response
    
if __name__ == '__main__':
    app.run(debug=True, port=5003)

