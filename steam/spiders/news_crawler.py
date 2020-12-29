
import scrapy
import configparser
import os, fnmatch
import re

config = configparser.RawConfigParser()
path = os.path.abspath(os.getcwd())
config.read('/'.join((path.split('/')[:-2]))+'/scrapy.cfg')
html_file_path = '/'.join((path.split('/')[:-2]))

class QuotesSpider(scrapy.Spider):
    name = "sc"
    lst = []
    urls = []
    visited_links_set = set()
    to_visit_links_set = set()
    failed_urls = []
    games_dict = {}

    def start_requests(self):
        games =  dict(config.items('games'))
        for game_name in games:
            self.urls.append('https://steamcommunity.com/app/'+games[game_name])
            self.games_dict[games[game_name]] = game_name

        for url in self.urls:
            self.visited_links_set.add(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.status == 400:
            print("failed with 400", response.url)
            yield scrapy.Request(url=response.url, callback=self.parse)
            self.failed_urls.append(response.url)

        if response.status == 404:
            print("failed with 404", response.url)
            self.failed_urls.append(response.url)

        if response.status == 403:
            print("failed with 403", response.url)
            self.failed_urls.append(response.url)

        filename = html_file_path + '/sc_'+self.games_dict[response.request.url.split('/')[4]]+'.html'
        base_url = 'https://steamcommunity.com/app/'+ response.request.url.split('/')[4]
        self.lst.append(response.body.__str__()+"****break****")

        links = response.css('a::attr(href)').getall()
        cleaned_links = [t for t in links if (base_url in t) and (t not in self.visited_links_set)]
        for link in cleaned_links:
            if link not in self.visited_links_set:
                self.to_visit_links_set.add(link)
        self.to_visit_links_set = self.to_visit_links_set - self.visited_links_set
        # print(cleaned_links)
        for link in self.to_visit_links_set:
            if 'https:' in link and link not in self.urls:
                self.visited_links_set.add(link)
                yield scrapy.Request(url=link, callback=self.parse)

        print(self.visited_links_set)
        with open(filename, 'a') as f:
            f.write(self.lst.__str__())

            self.lst = []
