# Web Performance Check Tool

## Overview
This tool is designed to automate the process of web performance testing. It uses Node.js for scraping web performance data, Python for processing and analyzing this data, and a Flask web server for managing the application and displaying results.

## Project Structure
- `/scraper`: Node.js scripts for web scraping.
- `/analysis-python`: Python scripts for data analysis.
- `/data`: Storage for raw data collected by the scraper.
- `/web-flask`: Flask application for the web interface.

## Setup Instructions

### Prerequisites
- Node.js
- Python 3.x
- npm
- pip

### Setting Up the Node.js Scraper
```bash
cd scraper
npm install
```

## Setting Up the Python Analysis

```
cd analysis-python
pip install -r requirements.txt
```

## Setting Up the Flask Web Server
```
cd web-flask
pip install -r requirements.txt
export FLASK_APP=app.py
flask run
```










