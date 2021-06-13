import logging

from torrentcrawler.items import TorrentObject

import scrapy
import scrapy.exceptions
import scrapy.linkextractors.lxmlhtml


class RutrackerSpider(scrapy.spiders.CrawlSpider):
    name = "rutracker-spider"
    allowed_domains = ["rutracker.org"]

    login_url = "http://rutracker.org/forum/login.php"
    start_urls = ["http://rutracker.org/forum/tracker.php"]

    rutracker_login = "notkeddad_bot"
    rutracker_password = "5MY9TB2YWjDswQ"

    bad_pages_regexp = r"http:\/\/rutracker\.org\/forum\/(login\.php|privmsg\.php|groupcp\.php|info\.php|dl\.php)"

    rules = [
        scrapy.spiders.Rule(scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor(deny=bad_pages_regexp), callback="parse_data", follow=True)
    ]

    def start_requests(self):
        yield scrapy.FormRequest(url=self.login_url,
                                 formdata={"login_username": self.rutracker_login,
                                           "login_password": self.rutracker_password,
                                           "login": "%C2%F5%EE%E4"},
                                 callback=self.check_login_response)

    def check_login_response(self, response: scrapy.http.response.Response):
        if response.css("a#logged-in-username::text").get() == self.rutracker_login:
            self.log(f"Logged in on Rutracker as {self.rutracker_login}")
            return [scrapy.Request(url=x) for x in self.start_urls]  # wtf
        else:
            self.log(f"Unable to log in on Rutracker", level=logging.ERROR)
            raise scrapy.exceptions.CloseSpider

    def parse_data(self, response: scrapy.http.response.Response):
        magnet = response.css("a.magnet-link::attr(title)").extract_first()

        if magnet is not None:
            yield TorrentObject(name=response.xpath("//a[@id='topic-title']/descendant-or-self::*/text()").get(),
                                size=int(response.css("span#tor-size-humn::attr(title)").extract_first()),
                                reg=response.xpath("//a[contains(@class, 'p-link small')]/text()").get(),
                                hash=magnet,
                                seeders=int(response.css("span.seed > b::text").get() or "0"),
                                leeches=int(response.css("span.leech > b::text").get() or "0"),
                                url=response.url)

