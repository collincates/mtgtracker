from scraper.scraper.items import PriceItem

# from scraper.spiders.cfb_spider import CFBSpider

class PricePipeline(object):
    def process_item(self, item, spider):
        # raise ValueError('DASFD')
        item.save()
        return item


class LogWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('captureditems.log', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = str(item.__dict__['_values']) + "\n"
        self.file.write(line)
        return item
