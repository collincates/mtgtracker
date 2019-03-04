from django.core.management.base import BaseCommand
from scraper.scraper.spiders.cfb_spider import CFBSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        process = CrawlerProcess(get_project_settings())
        process.crawl(CFBSpider)
        process.start()
