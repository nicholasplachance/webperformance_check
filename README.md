# Performance Testing Microservice

Performance Testing Microservice is a Flask-based web application that allows users to conduct performance tests on web pages. It utilizes Selenium for web scraping to gather performance metrics such as load time.

## Features

- Conduct performance tests on web pages
- Measure load time for each test iteration
- Specify the number of iterations for a test

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd PerformanceTestingMicroservice
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server:**
   ```bash
   python app.py
   ```

## Usage

To initiate a performance test, send a POST request to the `/test` endpoint with a JSON payload containing the URL to test and the number of iterations (optional). Here's an example using cURL:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.example.com", "repeat": 3}' http://127.0.0.1:5000/test

curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.hellhades.com", "repeat": 3}' http://127.0.0.1:5000/test
```

Replace `"https://www.example.com"` with the URL you want to test, and `"repeat": 3` with the number of iterations.

## Requirements

The following Python packages are required to run the application:

- Flask==2.0.2
- Selenium==4.1.0

You can install them using pip:

```bash
pip install -r requirements.txt
```

## Planned Features

- Add support for collecting additional performance metrics
- Implement graphical representation of performance metrics
- Enhance error handling and response messages
