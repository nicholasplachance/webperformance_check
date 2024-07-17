const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  let browser;  // Define browser variable in the broader scope

  try {
    const urls = JSON.parse(process.argv[2]);
    if (!urls || !urls.length) throw new Error('Please provide a list of URLs as an argument');

    browser = await puppeteer.launch();  // Initialize browser
    const results = [];

    for (const url of urls) {
      const page = await browser.newPage();
      const requests = [];

      page.on('request', request => {
        requests.push({ url: request.url(), method: request.method(), type: request.resourceType(), startTime: new Date().getTime() });
      });

      page.on('response', response => {
        const req = requests.find(r => r.url === response.url());
        if (req) {
          req.endTime = new Date().getTime();
          req.duration = req.endTime - req.startTime;
        }
      });

      await page.goto(url, { waitUntil: 'networkidle2' });

      const title = await page.title();
      const visitedUrl = page.url();
      const performanceMetrics = await page.metrics();
      const timestamp = new Date(performanceMetrics.Timestamp * 1000).toLocaleString();
      const taskDuration = (performanceMetrics.TaskDuration * 1000).toFixed(2);
      const performanceTiming = JSON.parse(await page.evaluate(() => JSON.stringify(window.performance.timing)));
      const ttfb = performanceTiming.responseStart - performanceTiming.navigationStart;
      const fcp = performanceTiming.domContentLoadedEventEnd - performanceTiming.navigationStart;
      const lcp = performanceTiming.loadEventEnd - performanceTiming.navigationStart;
      const heapAllocation = (performanceMetrics.JSHeapUsedSize / performanceMetrics.JSHeapTotalSize) * 100;

      const metrics = {
        title,
        url: visitedUrl,
        taskDuration: `${taskDuration} ms`,
        timestamp,
        ttfb: `${ttfb} ms`,
        fcp: `${fcp} ms`,
        lcp: `${lcp} ms`,
        heapAllocation: `${Math.round(heapAllocation)}%`,
        requests: requests.map(req => ({ url: req.url, method: req.method, type: req.type, startTime: req.startTime, duration: req.duration }))
      };

      results.push(metrics);
      await page.close();
    }

    const filePath = path.resolve(__dirname, '../data/raw_metrics.json');
    fs.writeFileSync(filePath, JSON.stringify(results, null, 2));
    console.log('Metrics written successfully');
  } catch (error) {
    console.error('Error during scraping:', error.message);
    process.exit(1);
  } finally {
    if (browser) {
      await browser.close();  // Close browser if it was initialized
    }
  }
})();
