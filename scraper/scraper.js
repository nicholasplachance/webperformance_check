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

  try {
    console.log(`Navigating to URL: ${url}`);
    await page.goto(url, { waitUntil: 'networkidle2' });

    const title = await page.title();
    console.log('Page title:', title);

    const visitedUrl = page.url();
    console.log('URL visited:', visitedUrl);

    const performanceMetrics = await page.metrics();
    const timestamp = performanceMetrics.Timestamp;
    const taskDuration = performanceMetrics.TaskDuration;
    console.log("Task duration: ", taskDuration);
    console.log("Timestamp: ", timestamp);

    const metrics = {
      title: title,
      url: visitedUrl,
      taskDuration: taskDuration,
      timestamp: timestamp
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





// TODO
// METRICS TO GRAB
// Speed Index | TTFB | FCP | LCP | Waterfall

