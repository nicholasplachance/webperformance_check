#!/bin/bash

# Ensure node is available
NODE_PATH=${NODE_PATH:-$(which node)}
SCRAPER_PATH=${SCRAPER_PATH:-./scraper/scraper.js}

# Run the scraper script
$NODE_PATH $SCRAPER_PATH $1
