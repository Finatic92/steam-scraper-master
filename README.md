# Steam Scraper

This repository contains [Scrapy](https://github.com/scrapy/scrapy) spiders for **crawling products** and **scraping all user-submitted reviews** from the [Steam game store](https://steampowered.com).
A few scripts for more easily managing and deploying the spiders are included as well.

This repository contains code accompanying the *Scraping the Steam Game Store* article published on the [Scrapinghub blog](https://blog.scrapinghub.com/2017/07/07/scraping-the-steam-game-store-with-scrapy/) and the [Intoli blog](https://intoli.com/blog/steam-scraper/).

## Installation

After cloning the repository with
```bash
git clone git@github.com:Finatic92/steam-scraper-master.git
```
start and activate a Python 3.6+ virtualenv with
```bash
cd steam-scraper
virtualenv -p python3.6 env
. env/bin/activate
```
Install Python requirements via:
```bash
pip install -r requirements.txt
```

By the way, on macOS you can install Python 3.6 via [homebrew](https://brew.sh):
 ```bash
 brew install python3
```
On Ubuntu you can use [instructions posted on askubuntu.com](https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get).


Using the Steam Crawler:
```
to crawl the site and use the spider crawler use command: scrapy crawl sc 
in terminal in this path.
```
The Config.cfg file has the names of each game that can be crawled along with the steam ID for that game. 
New games can be added.

DataProcessing.py file is run to generate the .csv files that would contain the crawled data for certain keywords.
The Keyword list can be enhanced to add more keywords in the DataProcessing.py file. 
Just add more comma-seperated keywords in the list.

```
Run the main fuinction of this class once all game sites have been crawled. 
```

Flow of control:
```
1. First run the command : scrapy crawl sc : to crawl through each of the games. Once .html file is generated for each game,
2. run the main method of file DataProcessing.py.
```
