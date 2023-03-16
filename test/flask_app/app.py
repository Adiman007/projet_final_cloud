from flask import Flask, render_template, request, session
import time
from pymongo import MongoClient


app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient('mongodb://mongodb-container:27017/')
db = client['clicks_db']
performance = db['clicks_collection']

with open('data/name.txt') as f:
    lines = f.read()
    # Return the fetched data as a string

name = lines.strip("\n")

if(name == None or name == ""):
    name = "guest"

@app.route('/', methods=['GET', 'POST'])
def index():
    print("ça fonctionne frérot")
    if request.method == 'POST':
        # Increment the counter in the session
        session['counter'] = session.get('counter', 0) + 1
    # Check if the time limit has been reached
    if session.get('start_time', 0) == 0:
        session['start_time'] = time.time()
    elapsed_time = time.time() - session['start_time']
    

    if elapsed_time >= 10:
        # Store the counter value in the session
        session['final_counter'] = session.get('counter', 0)
        performance.insert_one({'name': name , 'count': session['final_counter']})
        # Reset the counter and start time
        session['counter'] = 0
        session['start_time'] = 0
    return render_template('index.html', counter=session.get('counter', 0), elapsed_time=elapsed_time)

@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    all_score = performance.find()
    print(all_score)
    sorted_scores = sorted(all_score.items(), key=lambda x: x[1], reverse=True)
    print(sorted_scores)
    return render_template('leaderboard.html', all_score=sorted_scores)


if __name__ == '__main__':
    print("ça fonctionne frérot !!!")
    app.run(host='0.0.0.0')
