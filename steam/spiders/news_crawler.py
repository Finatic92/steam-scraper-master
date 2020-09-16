
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "sn"

    def start_requests(self):
        urls = [
            'http://steamcommunity.com/app/227680/eventcomments/1631915072539961227'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #page = response.url.split("/")[-2]
        filename = 'sn.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        comments_string = response.css("div.commentthread_comment_text")
        all_comments = comments_string.css("::text").getall()
        patch_data = response.css("div.commentthread_comment_text")
        sn2 = response.css("div.responsive_page_content")
