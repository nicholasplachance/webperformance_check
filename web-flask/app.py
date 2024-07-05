from flask import Flask, request, redirect, url_for, render_template, flash
import subprocess
import json
import os
import validators

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_test', methods=['POST'])
def run_test():
    url = request.form['url']
    if not validators.url(url):
        flash('Invalid URL. Please enter a valid URL starting with http:// or https://')
        return redirect(url_for('index'))
    
    # Run the scraper script with the URL
    result = subprocess.run(['node', '../scraper/scraper.js', url], capture_output=True, text=True)
    
    if result.returncode != 0:
        flash('An error occurred while running the test: ' + result.stderr)
        return redirect(url_for('index'))

    print('Scraper output:', result.stdout)
    return redirect(url_for('report'))

@app.route('/report')
def report():
    if os.path.exists('../data/raw_metrics.json'):
        print('Metrics file found')
        with open('../data/raw_metrics.json') as f:
            try:
                data = json.load(f)
                # print('Metrics loaded:', data)
            except json.JSONDecodeError as e:
                flash(f'Error reading the metrics file: {e}')
                data = {}
    else:
        flash('Metrics file not found.')
        data = {}
    return render_template('report.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
