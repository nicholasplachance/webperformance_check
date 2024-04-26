# app.py

from flask import Flask, request
from selenium_script import gather_performance_metrics 

class PerformanceTestingMicroservice:
    # constructor method - initialize Flask and setup routes
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    # responsible for setting up routes for the app - add_url_rule is a Flask method to define routes and associate them with view functions 
    def setup_routes(self):
        self.app.add_url_rule('/', view_func=self.index)
        self.app.add_url_rule('/test', view_func=self.initate_test, methods=['POST'])

    # handler for the rool URL ('/')
    def index(self):
        return "Welcome to the Performance Testing Microservice!"
    
    def initate_test(self):
        # Assuming the client sends a JSON payload with the URL to test
        data = request.json
        if 'url' in data:
            url = data['url']
            repeat = data.get('repeat', 1)  # Default to run the test once if 'repeat' parameter is not provided
            repeat = int(repeat)  # Convert the repeat parameter to an integer
            results = []
            for _ in range(repeat):
                performance_metrics = gather_performance_metrics(url)
                results.append(performance_metrics)
            return {"results": results}
        else:
            return "Error: 'url' parameter missing in request payload", 400
    
    # starts the server to run the app
    def run(self):
        self.app.run(debug=True)



if __name__ == '__main__':
    performance_testing_microservice = PerformanceTestingMicroservice()
    performance_testing_microservice.run()