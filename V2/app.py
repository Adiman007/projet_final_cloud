from flask import Flask, render_template, request, session
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
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
        # Reset the counter and start time
        session['counter'] = 0
        session['start_time'] = 0
    return render_template('index.html', counter=session.get('counter', 0), elapsed_time=elapsed_time)

if __name__ == '__main__':
    app.run()
