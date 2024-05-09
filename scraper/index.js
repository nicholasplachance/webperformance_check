const express = require('express');
const { exec } = require('child_process');
const app = express();

app.get('/start-scraping', async (req, res) => {
    // Trigger scraping logic
    const data = await scrapeData(); // Assume this function handles scraping
    saveData(data); // Saves data to a file or database

    // Optionally trigger Python script
    exec('python generate_report.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send('Error generating report');
        }
        res.send('Report generated successfully');
    });
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
