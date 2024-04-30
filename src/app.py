from flask import Flask, request, send_file, make_response
from selenium_script import gather_performance_metrics 
from generate_report import generate_html_report
import os
import shutil
import zipfile

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
    
    def initiate_test(self):
        # Assuming the client sends a JSON payload with the URL to test
        data = request.json
        if 'url' in data:
            url = data['url']
            repeat = int(data.get('repeat', 1))  # Default to run the test once if 'repeat' parameter is not provided
            results = []
            for _ in range(repeat):
                performance_metrics = gather_performance_metrics(url)
                results.append(performance_metrics)
            
            # Generate HTML report
            report_path = generate_html_report(results, url, 'performance_report.html')
            
            # Create a folder for the reports
            reports_folder = 'webspeedinsight_reports'
            if not os.path.exists(reports_folder):
                os.makedirs(reports_folder)

            # Move the HTML report to the reports folder
            shutil.move(report_path, os.path.join(reports_folder, 'performance_report.html'))

            # Zip the reports folder
            zip_filename = 'webspeedinsight_reports.zip'
            zip_path = os.path.abspath(zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for root, dirs, files in os.walk(reports_folder):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), reports_folder))
            
            # Send the zip file as an attachment
            response = make_response(send_file(zip_path, as_attachment=True))
            response.headers['Content-Disposition'] = f'attachment; filename={zip_filename}'
            return response
        else:
            return "Error: 'url' parameter missing in request payload", 400
    
    # starts the server to run the app
    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    performance_testing_microservice = PerformanceTestingMicroservice()
    performance_testing_microservice.run()
