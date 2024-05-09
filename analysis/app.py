import json
import os
import shutil
import zipfile
import tempfile
from flask import Flask, request, send_file, make_response
from selenium_script import gather_performance_metrics 
from generate_report import generate_html_report
import re
import time

class PerformanceTestingMicroservice:
    # constructor method - initialize Flask and setup routes
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    # responsible for setting up routes for the app
    def setup_routes(self):
        self.app.add_url_rule('/', view_func=self.index)
        self.app.add_url_rule('/test', view_func=self.initiate_test, methods=['POST'])

    # handler for the root URL ('/')
    def index(self):
        return "Welcome to the Performance Testing Microservice!"
    
    

    def generate_and_send_report(self, url, results):
        # Extract performance metrics and screenshot paths from each tuple in results
        performance_metrics_list = [result[0] for result in results]
        screenshot_paths = [result[1] for result in results]
        
        # Create a temporary folder to store screenshots
        temp_folder = tempfile.mkdtemp()
        
        # Copy screenshots to the temporary folder and collect their new paths
        new_screenshot_paths = []
        for screenshot_path in screenshot_paths:
            new_screenshot_path = os.path.join(temp_folder, os.path.basename(screenshot_path))
            shutil.copyfile(screenshot_path, new_screenshot_path)
            new_screenshot_paths.append(new_screenshot_path)

        # Generate HTML report using the new screenshot paths
        report_path = generate_html_report(performance_metrics_list, url, new_screenshot_paths[0])

        # Create a zip file containing the HTML report and screenshots
        sanitized_time = re.sub(r'[^a-zA-Z0-9]', '_', time.strftime("%Y%m%d-%H%M%S"))
        zip_filename = f'webspeedinsight_reports_{sanitized_time}.zip'
        zip_path = os.path.join(temp_folder, zip_filename)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(report_path, os.path.basename(report_path))  # Include the HTML report in the zip
            for screenshot_path in new_screenshot_paths:
                zipf.write(screenshot_path, os.path.basename(screenshot_path))  # Include each screenshot in the zip
        
        return zip_path

    def send_zip_file(self, zip_path):
        response = make_response(send_file(zip_path, as_attachment=True))
        response.headers['Content-Disposition'] = f'attachment; filename=webspeedinsight_reports.zip'
        return response
    

    def initiate_test(self):
        data = request.json
        if 'url' in data:
            url = data['url']
            js_script = data.get('js_script', '')
            repeat = int(data.get('repeat', 1))  # Default to run the test once if 'repeat' parameter is not provided
            results = []
            for _ in range(repeat):
                performance_metrics = gather_performance_metrics(url, js_script)
                results.append(performance_metrics)
            
            try:
                zip_path = self.generate_and_send_report(url, results)
                return self.send_zip_file(zip_path)
            except Exception as e:
                return f"Error: {str(e)}", 500
        else:
            return "Error: 'url' parameter missing in request payload", 400

    
    # starts the server to run the app
    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    performance_testing_microservice = PerformanceTestingMicroservice()
    performance_testing_microservice.run()
