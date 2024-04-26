from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

def gather_performance_metrics(url):
    driver = webdriver.Chrome()

    # navigate to url
    driver.get(url)

    # wait for page to load completely
    time.sleep(5)

    # get perfromance timing data
    timing = driver.execute_script("return window.performance.timing")

    # calculate laod time and other metrics
    navigation_start = timing['navigationStart']
    load_event_end = timing['loadEventEnd']
    load_time = load_event_end - navigation_start # in miliseconds


    # extract other relevant metrics if needed

    # close webdriver
    driver.quit()

    metrics = {
        'load_time': load_time,
        # more to be added here
    }

    return metrics

if __name__ == '__main__':
    # test the function with google.com
    url = 'https://www.google.com'
    performance_metrics = gather_performance_metrics(url)
    print("Performance Metrics for", url)
    print("Load Time:", performance_metrics['load_time'], "miliseconds")