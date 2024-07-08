const express = require('express');
const { exec } = require('child_process');
const app = express();

app.get('/start-scraping', async (req, res, next) => {
  try {
    const data = await scrapeData();
    saveData(data);

    exec('python generate_report.py', (error, stdout, stderr) => {
      if (error) {
        next(new Error('Error generating report: ' + error.message));
      } else {
        res.send('Report generated successfully');
      }
    });
  } catch (error) {
    next(error);
  }
});

app.use((err, req, res, next) => {
  console.error(err.message);
  res.status(500).send('Internal Server Error');
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
