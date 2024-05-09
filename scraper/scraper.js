const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Navigate to the page
  await page.goto('https://hellhades.com');

  // Get and print the page title
  const title = await page.title();
  console.log('Page title:', title);

  // Get and print the URL of the page to ensure it is the intended page
  const url = page.url();
  console.log('URL visited:', url);

  const performanceMetrics = page.metrics()
  const timestamp = (await performanceMetrics).Timestamp
  const taskDuration = (await performanceMetrics).TaskDuration
  console.log("Task duration: ", taskDuration);
  console.log("Timestamp: ", timestamp);

  // Close the browser
  await browser.close();
})();
