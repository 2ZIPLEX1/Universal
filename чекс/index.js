// render.js
const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto(`file://${__dirname}/index.html`, { waitUntil: 'networkidle0' });

  await page.setViewport({ width: 375, height: 812 }); // iPhone X размер

  await page.screenshot({ path: 'screenshot.png' });

  await browser.close();
})();
