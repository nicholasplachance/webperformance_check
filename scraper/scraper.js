const puppeteer = require("puppeteer");

async function scrapePerformanceMetrics(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url);
    // perform task similiar to python's selenium script
    await browser.close();
}