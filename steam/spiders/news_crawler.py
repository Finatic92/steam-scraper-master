
import scrapy
import configparser
import re

config = configparser.RawConfigParser()
config.read('/Users/pranaykhattri/Downloads/NLP_RA/steam-scraper-master/scrapy.cfg')

class QuotesSpider(scrapy.Spider):
    name = "sc"
    lst = []
    urls = []
    visited_links_set = set()
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
        filename = 'sc_'+self.games_dict[response.request.url.split('/')[4]]+'.html'
        base_url = 'https://steamcommunity.com/app/'+ response.request.url.split('/')[4]

        self.lst.append(response.body)

        links = response.css('a::attr(href)').getall()
        cleaned_links = [t for t in links if (base_url in t) and (t not in self.visited_links_set)]
        print(cleaned_links)
        for link in cleaned_links:
            if 'https:' in link and link not in self.urls:
                self.visited_links_set.add(link)
                yield scrapy.Request(url=link, callback=self.parse)

        print(self.visited_links_set)
        with open(filename, 'a') as f:
            f.write(self.lst.__str__())
            self.lst = []

        # self.log('Saved file %s' % filename)
        # comments_string = response.css("div.commentthread_comment_text")
        # all_comments = comments_string.css("::text").getall()
        # patch_data = response.css("div.commentthread_comment_text")
        # sn2 = response.css("div.responsive_page_content")
