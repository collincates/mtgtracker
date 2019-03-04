import scrapy
from price.models import Card, Condition, Vendor
from scraper.scraper.items import PriceItem

import datetime


class CFBSpider(scrapy.Spider):
    name= 'cfb_spider'
    start_urls = ['https://store.channelfireball.com/catalog/magic_singles-core_sets-unlimited/68']

    def parse(self, response):
        cfb_vendor_object = Vendor.objects.get(code='CFB')
        cfb_conditions = Vendor.objects.get(code='CFB').conditions.all()
        data = response.css('li.product')

        for card_listing in data:
            for condition in cfb_conditions:
                price_model = PriceItem()
                price_model['card'] = Card.objects.filter(
                    # could use this instead of below:   card_listing.css('form.add-to-cart-form::attr(data-name)').get()
                    name=f'{card_listing.css("h4.name::text").get()}',
                    # 'set_name__contains' will find all sets that have the scraped
                    # word in them. How to deal with words that appear
                    # in multiple sets? An example of this is scraping the word
                    # 'Ravnica' and knowing there are sets called 'Ravnica',
                    # 'Return to Ravnica', 'Ravnica Allegiance', and maybe others
                    # planned for the future.
                    # 'set_name__contains' will return a single object in the case
                    # that there is only one set with this scraped name in it.
                    # In the example above, however, a Queryset of multiple sets
                    # will be returned.
                    set_name__contains=f'{response.css("meta.site-settings::attr(data-category)").get()}',
                ),
                price_model['vendor'] = cfb_vendor_object
                price_model['condition'] = Condition.objects.get(id=condition.id)

                # Is this the right way to check a card/condition's stock status?
                # This checks if the current from-database condition in our
                # iteration over cfb_conditions (which is a string like
                # 'Moderately Played', for example) is present on the page
                # in the data-variant attribute of the add-to-cart form.
                #
                # The data-variant string value format in this example is:
                #     'Moderately Played, English'
                #
                # So we are basically checking via regex if:
                #     'Moderately Played'  in   'Moderately Played, English'
                #     -------------------       ----------------------------
                #          condition       in   add-to-cart-form.data-variant
                #
                # The idea is that *if* there is an add-to-cart-form for this
                # card/condition, then a qty_in_stock and price *must* exist.
                #
                # A probable flaw for this setup is that if an add-to-cart-form
                # exists, but for whatever reason the string is misspelled or
                # mismatched on either side of the regex comparison, we will
                # overlook the value that is *actually* present in data-variant.
                #
                # TODO:
                # There is probably an html attribute somewhere that
                # declares a product out of stock, and a check for the
                # existence of this attribute will tell us definitely if the
                # card/condition's qty_in_stock and price do not exist.

                if card_listing.css('form.add-to-cart-form') and condition.name in card_listing.css('form.add-to-cart-form::attr(data-variant)').get():
                    price_model['qty_in_stock'] = int(card_listing.css('div.qty-submit input::attr(max)').get())
                    price_model['price'] = card_listing.css('form.add-to-cart-form::attr(data-price)').get().replace('$', '')
                else:
                    price_model['qty_in_stock'] = 0
                    price_model['price'] = None
                price_model['timestamp'] = datetime.datetime.now(datetime.timezone.utc)
                yield price_model

        # GO TO NEXT PAGE IF NEXT PAGE EXISTS

# if __name__ == "__main__":
#     spider = CFBSpider()
#     spider.parse()
