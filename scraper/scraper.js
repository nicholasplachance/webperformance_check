const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  const url = process.argv[2];
  if (!url) {
    console.error('Please provide a URL as an argument');
    process.exit(1);
  }

  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  const requests = [];

  // Listen for all network requests
  page.on('request', request => {
    requests.push({
      url: request.url(),
      method: request.method(),
      type: request.resourceType(),
      startTime: new Date().getTime() // Capture start time when request is initiated
    });
  });

  // Listen for all network requests that finished
  page.on('response', response => {
    const req = requests.find(r => r.url === response.url());
    if (req) {
      req.endTime = new Date().getTime();
      req.duration = req.endTime - req.startTime;
    }
  });

  try {
    console.log(`Navigating to URL: ${url}`);
    await page.goto(url, { waitUntil: 'networkidle2' });

    const title = await page.title();
    console.log('Page title:', title);

    const visitedUrl = page.url();
    console.log('URL visited:', visitedUrl);

    const performanceMetrics = await page.metrics();
    const timestamp = new Date(performanceMetrics.Timestamp * 1000).toLocaleString(); // Convert to human-readable format
    const taskDuration = (performanceMetrics.TaskDuration * 1000).toFixed(2); // Convert to milliseconds

    // Get performance timing metrics
    const performanceTiming = JSON.parse(await page.evaluate(() => JSON.stringify(window.performance.timing)));
    const ttfb = performanceTiming.responseStart - performanceTiming.navigationStart; // TTFB in milliseconds
    const fcp = performanceTiming.domContentLoadedEventEnd - performanceTiming.navigationStart; // FCP in milliseconds
    const lcp = performanceTiming.loadEventEnd - performanceTiming.navigationStart; // LCP in milliseconds
    const heapAllocation = (performanceMetrics.JSHeapUsedSize / performanceMetrics.JSHeapTotalSize) * 100; // Heap allocation percentage

    console.log("Task duration (ms): ", taskDuration);
    console.log("Timestamp: ", timestamp);
    console.log("TTFB (ms): ", ttfb);
    console.log("FCP (ms): ", fcp);
    console.log("LCP (ms): ", lcp);

    // Add resource timings to the metrics object
    const metrics = {
      title: title,
      url: visitedUrl,
      taskDuration: taskDuration + ' ms',
      timestamp: timestamp,
      ttfb: ttfb + ' ms',
      fcp: fcp + ' ms',
      lcp: lcp + ' ms',
      heapAllocation: Math.round(heapAllocation) + '%',
      requests: requests.map(req => ({
        url: req.url,
        method: req.method,
        type: req.type,
        startTime: req.startTime,
        duration: req.duration
      }))
    };

    const filePath = path.resolve(__dirname, '../data/raw_metrics.json');
    console.log(`Writing metrics to file: ${filePath}`);
    fs.writeFileSync(filePath, JSON.stringify(metrics, null, 2));
    console.log('Metrics written successfully');

  } catch (error) {
    console.error('Error navigating to the URL:', error);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
