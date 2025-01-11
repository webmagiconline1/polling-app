from flask import Flask, render_template, request, redirect, url_for
import redis

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    options = r.smembers('options')
    options = [option.decode('utf-8') for option in options]
    return render_template('index.html', options=options)

@app.route('/vote', methods=['POST'])
def vote():
    option = request.form['option']
    r.incr(option)
    return redirect(url_for('results'))

@app.route('/results')
def results():
    options = r.smembers('options')
    votes = {option.decode('utf-8'): int(r.get(option) or 0) for option in options}
    return render_template('results.html', votes=votes)

@app.route('/add_option', methods=['POST'])
def add_option():
    new_option = request.form['new_option']
    r.sadd('options', new_option)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)