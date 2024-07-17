# Web Performance Check Tool

## Overview
The Web Performance Check Tool automates the process of testing web performance. It combines web scraping, data analysis, and a user-friendly web interface to provide comprehensive insights into website performance metrics.

## Features
- **Web Scraping**: Uses Node.js and Puppeteer to collect performance metrics from websites.
- **Data Analysis**: Utilizes Python to process and analyze the collected data.
- **Web Interface**: Employs Flask to provide a web interface for running tests and viewing reports.

## Project Structure
    webperformance_check/
    ├── usr/
    |   ├── local
    |       ├── bin
    |           ├── node       
    ├── analysis-python/
    │ ├── analyze_data.py
    │ ├── requirements.txt
    ├── data/
    │ ├── raw_metrics.json
    │ ├── schema.sql
    ├── scraper/
    │ ├── index.js
    │ ├── package.json
    │ ├── scraper.js
    ├── web-flask/
    │ ├── app.py
    │ ├── config.py
    │ ├── requirements.txt
    │ ├── static/
    │ │ ├── style.css
    │ ├── templates/
    │ │ ├── index.html
    │ │ ├── report.html
    ├── README.md


## Prerequisites
- **Node.js** (version 14.x or higher)
- **Python 3.x**
- **npm** (Node Package Manager)
- **pip** (Python Package Installer)

## Setup Instructions

### Setting Up the Node.js Scraper
1. Navigate to the `scraper` directory:
   ```bash
   cd scraper
2. Install the required npm packages:
    ```
        npm install

### Setting Up the Python Analysis
1. Navigate to the `analysis-python` directory:
    ```
        cd analysis-python
2. Install the required Python packages:
    ```
        pip install -r requirements.txt

### Setting Up the Flask Web Server
1. Navigate to the `web-flask` directory:
    ```
        cd web-flask
2. Install the required Python packages:
    ```
        pip install -r requirements.txt
3. Set up and run the Flask application:
    ```
       export FLASK_APP=app.py
       flask run

## Usage

### Running the Web Scraper
1. Start the Node.js server:
   ```
    node scraper/index.js
2. Navigate to http://localhost:3000/start-scraping to initiate the scraping process.

### Analyzing Data
1. Run the Python analysis script:
    ```
        python analysis-python/analyze_data.py

### Viewing Reports
1. Open the Flask web interface in your browser:
    ```
        http://localhost:5000
2. Follow the on-screen instructions to run tests and view performance reports.    