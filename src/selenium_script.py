from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import json
import os

def gather_performance_metrics(url):
    # Initialize performance_metrics as an empty dictionary
    performance_metrics = {}

    driver = webdriver.Chrome()

    # navigate to url
    print(f"Navigating to URL: {url}")
    driver.get(url)

    # wait for page to load completely
    print("Waiting for page to load...")
    time.sleep(5)

    # get performance timing data
    timing = driver.execute_script("return window.performance.timing")
    print("Performance timing data:", timing)

    # calculate load time
    navigation_start = timing['navigationStart']
    load_event_end = timing['loadEventEnd']
    load_time = load_event_end - navigation_start # in milliseconds
    print("Load time:", load_time, "milliseconds")

    # close webdriver
    print("Closing webdriver...")
    driver.quit()

    # Add load time to performance metrics
    performance_metrics['load_time'] = load_time

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Specify the path to the JSON file inside the src directory
    json_file_path = os.path.join(current_dir, 'performance_metrics.json')

    # Export performance metrics to JSON file
    with open(json_file_path, 'w') as f:
        json.dump(performance_metrics, f)

    return performance_metrics

if __name__ == '__main__':
    # test the function with google.com
    url = 'https://www.google.com'
    print("Initiating performance test for:", url)
    performance_metrics = gather_performance_metrics(url)
    print("Performance Metrics for", url)
    print("Load Time:", performance_metrics['load_time'], "milliseconds")
