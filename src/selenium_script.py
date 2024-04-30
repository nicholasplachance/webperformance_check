import json
import os
import time
import shutil
from selenium import webdriver
import re

def gather_performance_metrics(url, js_script):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # Initialize performance_metrics as an empty dictionary
    performance_metrics = {}

    driver = webdriver.Chrome()

    # navigate to url
    print(f"Navigating to URL: {url}")
    driver.get(url)

    if js_script:
        driver.execute_script(js_script)

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

    # Capture additional metrics (e.g., TTFB, FCP, TTI)
    # Example:
    ttfb = timing['responseStart'] - timing['requestStart']
    fcp = timing['domContentLoadedEventStart'] - navigation_start
    tti = timing['domInteractive'] - navigation_start

    # Add metrics to performance_metrics dictionary
    performance_metrics['load_time'] = load_time
    performance_metrics['ttfb'] = ttfb
    performance_metrics['fcp'] = fcp
    performance_metrics['tti'] = tti

    # Capture screenshot
    sanitized_time = re.sub(r'[^a-zA-Z0-9]', '_', current_time)  
    screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'screenshot{sanitized_time}.png')
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved at: {screenshot_path}")

    # Move the screenshot to the 'screenshots' directory
    screenshots_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')
    os.makedirs(screenshots_dir, exist_ok=True)
    shutil.move(screenshot_path, screenshots_dir)

    # Construct the new path for the moved screenshot
    screenshot_path = os.path.join(screenshots_dir, os.path.basename(screenshot_path))

    # close webdriver
    print("Closing webdriver...")
    driver.quit()

    return performance_metrics, screenshot_path

if __name__ == '__main__':
    # test the function with google.com
    url = 'https://www.google.com'
    print("Initiating performance test for:", url)
    performance_metrics, screenshot_path = gather_performance_metrics(url, '')
    
    # Combine performance metrics and screenshot path into a single dictionary
    combined_data = {
        'performance_metrics': performance_metrics,
        'screenshot_path': screenshot_path
    }

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Specify the path to the JSON file inside the src directory
    json_file_path = os.path.join(current_dir, 'performance_data.json')

    # Export combined data to JSON file
    with open(json_file_path, 'w') as f:
        json.dump(combined_data, f)
