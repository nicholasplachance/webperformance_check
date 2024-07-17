from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
import subprocess
import json
import os
import validators
import logging
import statistics
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

logging.basicConfig(level=logging.INFO)

# Function to extract favicon URL from HTML
def get_favicon(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        favicon_tag = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
        if favicon_tag:
            return favicon_tag['href']
        return None
    except Exception as e:
        logging.error(f'Error fetching favicon for {url}: {e}')
        return None

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_test', methods=['POST'])
def run_test():
    base_url = request.form['base_url']
    pages = request.form.getlist('pages[]')
    urls = [base_url] + [base_url.rstrip('/') + page for page in pages]

    invalid_urls = [url for url in urls if not validators.url(url)]
    if invalid_urls:
        flash(f'Invalid URLs: {", ".join(invalid_urls)}. Please enter valid URLs starting with http:// or https://')
        return redirect(url_for('index'))

    favicon_urls = {}
    for url in urls:
        favicon_url = get_favicon(url)
        if favicon_url:
            favicon_urls[url] = favicon_url

    try:
        result = subprocess.run(['node', '../scraper/scraper.js', json.dumps(urls)], capture_output=True, text=True)
        result.check_returncode()
        print('Scraper output:', result.stdout)
        return redirect(url_for('report', favicon_urls=json.dumps(favicon_urls)))
    except subprocess.CalledProcessError as e:
        flash(f'An error occurred while running the test: {e.stderr}')
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f'Unexpected error: {e}')
        flash('An unexpected error occurred. Please try again later.')
        return redirect(url_for('index'))

@app.route('/report')
def report():
    favicon_urls = json.loads(request.args.get('favicon_urls', '{}'))
    
    if os.path.exists('../data/raw_metrics.json'):
        with open('../data/raw_metrics.json') as f:
            try:
                data = json.load(f)
                metrics = ['ttfb', 'fcp', 'lcp', 'taskDuration', 'heapAllocation']
                average_metrics = {}
                for metric in metrics:
                    values = []
                    for page in data:
                        value = page[metric].split()[0]
                        if metric == 'heapAllocation':
                            value = value.rstrip('%')
                        values.append(float(value))
                    average_metrics[metric] = statistics.mean(values)
            except json.JSONDecodeError as e:
                flash(f'Error reading the metrics file: {e}')
                data = []
                average_metrics = {}
    else:
        flash('Metrics file not found.')
        data = []
        average_metrics = {}

    return render_template('report.html', data=data, average_metrics=average_metrics, favicon_urls=favicon_urls)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
import subprocess
import json
import os
import validators
import logging
import statistics
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

logging.basicConfig(level=logging.INFO)

# Function to extract favicon URL from HTML
def get_favicon(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        favicon_tag = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
        if favicon_tag:
            return favicon_tag['href']
        return None
    except Exception as e:
        logging.error(f'Error fetching favicon for {url}: {e}')
        return None

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_test', methods=['POST'])
def run_test():
    base_url = request.form['base_url']
    pages = request.form.getlist('pages[]')
    urls = [base_url] + [base_url.rstrip('/') + page for page in pages]

    invalid_urls = [url for url in urls if not validators.url(url)]
    if invalid_urls:
        flash(f'Invalid URLs: {", ".join(invalid_urls)}. Please enter valid URLs starting with http:// or https://')
        return redirect(url_for('index'))

    favicon_urls = {}
    for url in urls:
        favicon_url = get_favicon(url)
        if favicon_url:
            favicon_urls[url] = favicon_url

    try:
        result = subprocess.run(['node', '../scraper/scraper.js', json.dumps(urls)], capture_output=True, text=True)
        result.check_returncode()
        print('Scraper output:', result.stdout)
        return redirect(url_for('report', favicon_urls=json.dumps(favicon_urls)))
    except subprocess.CalledProcessError as e:
        flash(f'An error occurred while running the test: {e.stderr}')
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f'Unexpected error: {e}')
        flash('An unexpected error occurred. Please try again later.')
        return redirect(url_for('index'))

@app.route('/report')
def report():
    favicon_urls = json.loads(request.args.get('favicon_urls', '{}'))
    
    if os.path.exists('../data/raw_metrics.json'):
        with open('../data/raw_metrics.json') as f:
            try:
                data = json.load(f)
                metrics = ['ttfb', 'fcp', 'lcp', 'taskDuration', 'heapAllocation']
                average_metrics = {}
                for metric in metrics:
                    values = []
                    for page in data:
                        value = page[metric].split()[0]
                        if metric == 'heapAllocation':
                            value = value.rstrip('%')
                        values.append(float(value))
                    average_metrics[metric] = statistics.mean(values)
            except json.JSONDecodeError as e:
                flash(f'Error reading the metrics file: {e}')
                data = []
                average_metrics = {}
    else:
        flash('Metrics file not found.')
        data = []
        average_metrics = {}

    return render_template('report.html', data=data, average_metrics=average_metrics, favicon_urls=favicon_urls)

if __name__ == '__main__':
    app.run(debug=True)
