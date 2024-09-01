# xbox-game-scraper
This Python script uses Playwright to scrape game titles and cover images URLs from the Xbox website, dumping them into a CSV file.

## Requirements
* Playwright: Install using `pip install playwright`
* Browser:  Playwright will automatically download the necessary browser binaries (Chromium, Firefox, or WebKit).

## Usage
```
pip install -r requiremets.txt
python scrape-xbox.py
```
The scraped data will be saved in xbox_game_titles.csv.