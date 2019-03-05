from scraper.scraper.items import PriceItem

# from scraper.spiders.cfb_spider import CFBSpider

class PricePipeline(object):
    def process_item(self, item, spider):
        # raise ValueError('DASFD')
        item.save()
        return item
