from flask import Flask, render_template, request, redirect, url_for
import redis

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    option = request.form['option']
    r.incr(option)
    return redirect(url_for('results'))

@app.route('/results')
def results():
    votes = {
        'option1': int(r.get('option1') or 0),
        'option2': int(r.get('option2') or 0),
        'option3': int(r.get('option3') or 0)
    }
    return render_template('results.html', votes=votes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)