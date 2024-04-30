import json
import os
import uuid  # For generating unique identifiers
import time
import re  # For replacing invalid characters in filenames

def generate_html_report(performance_metrics, url, screenshot_path):
    # generate HTML report dynamically
    html_content = f"""
    <html>
    <head>
        <title>Performance Test Report</title>
    </head>
    <body>
        <h1>Performance Test Report</h1>
        <p> URL Tested: </p><a href="{url}">{url}<a/>
    """
    
    # Add current time (CST) to the HTML content
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    html_content += f"<p>Test ran at: {current_time} (CST)</p>"
    
    # Display screenshot if available
    if screenshot_path:
        # Add width and height attributes to limit the size of the screenshot
        html_content += f'<p>Screenshot:</p><img src="{screenshot_path}" alt="Screenshot" width="500" height="500">'
    
    # Iterate over each performance metric and add it to the HTML content
    for metric in performance_metrics:
        html_content += f"<p>Load Time: {metric.get('load_time', 'N/A')} ms</p>"
        html_content += f"<p>TTFB: {metric.get('ttfb', 'N/A')} ms</p>"
        html_content += f"<p>FCP: {metric.get('fcp', 'N/A')} ms</p>"
        html_content += f"<p>TTI: {metric.get('tti', 'N/A')} ms</p>"
        # Add more performance metrics here if needed
    
    # Close the HTML tags
    html_content += """
    </body>
    </html>
    """

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Specify the path to the reports directory
    reports_dir = os.path.join(current_dir, 'reports')
    
    # Create the reports directory if it doesn't exist
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Generate a unique filename for the HTML report
    sanitized_time = re.sub(r'[^a-zA-Z0-9]', '_', current_time)  # Replace invalid characters with underscores
    unique_filename = sanitized_time + '_webspeedinsight.html'
    
    # Specify the path to the HTML report file
    report_path = os.path.join(reports_dir, unique_filename)

    # Save HTML report to file 
    with open(report_path, 'w') as f:
        f.write(html_content)

    return report_path

