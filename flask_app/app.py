from flask import Flask, render_template, request, session
import time
from pymongo import MongoClient


app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient('mongodb://mongodb-container:27017/')
db = client['clicks_db']
performance = db['clicks_collection']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['counter'] = session.get('counter', 0) + 1

    if session.get('start_time', 0) == 0:
        session['start_time'] = time.time()
    elapsed_time = time.time() - session['start_time']
    

    if elapsed_time >= 10:
        session['final_counter'] = session.get('counter', 0)

        with open('data/name.txt') as f:
            lines = f.read()
        f.close()

        name = lines.strip("\n")

        print(name)


        if(name == None or name == ""):
            name = "guest"

        print(name)
        performance.insert_one({'name': name , 'count': session['final_counter']})

        session['counter'] = 0
        session['start_time'] = 0
    return render_template('index.html', counter=session.get('counter', 0), elapsed_time=elapsed_time)

@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    all_score = performance.find()
    
    print(all_score)
    sorted_scores = sorted(all_score, key=lambda x: x['count'], reverse=True)
    print(sorted_scores)
    return render_template('leaderboard.html', all_score=sorted_scores)


if __name__ == '__main__':
    print("app is running")
    app.run(host='0.0.0.0')
