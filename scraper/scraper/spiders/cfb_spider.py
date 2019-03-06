import re
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
        card_list = response.css('li.product')

        for card_listing in card_list:
            for condition in cfb_conditions:
                try:
                    price_model = PriceItem()
                    price_model['card'] = Card.objects.get(
                        # could use this instead of below:   card_listing.css('form.add-to-cart-form::attr(data-name)').get()
                        # Strip non-alphanumeric characters from card_listing's h4 card name
                        name__iregex=fr"{re.sub('[^0-9a-zA-Z]+', '.+', card_listing.css('h4.name::text').get())}",
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
                        set_name__contains=f'{response.css("meta.site-settings::attr(data-category)").get()}'
                    )
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
                    # So we are basically checking via regex stripping if:
                    #     'Moderately Played'  ==   'Moderately Played'(, English)
                    #     -------------------       ----------------------------
                    #          condition       ==   add-to-cart-form.data-variant
                    #
                    # The idea is that *if* there is an add-to-cart-form for this
                    # card/condition, then a qty_in_stock and price *must* exist.
                    #
                    # A probable flaw for this setup is that if an add-to-cart-form
                    # exists, but for whatever reason the string is misspelled or
                    # mismatched on either side of the regex comparison, we will
                    # overlook the value that is *actually* present in data-variant
                    # and instead list the card/condition as out of stock.

                    # HTML "div.variant-row.row.no-stock" is only present in cases
                    # where the item is definitely out of stock.
                    if card_listing.css("div.variant-row.row.no-stock"):
                        price_model['qty_in_stock'] = 0
                        price_model['price'] = None
                    else:
                        # There are various conditions for sale
                        for variant in card_listing.css("div.variants div.variant-row.row"):
                            # Compare database condition string to add-to-cart form
                            # as per the example in the big comment just above here.
                            if condition.name == variant.css('form.add-to-cart-form::attr(data-variant)').re(r'(.*),')[0]:
                                price_model['qty_in_stock'] = int(variant.css('div.qty-submit input::attr(max)').get())
                                price_model['price'] = variant.css('form.add-to-cart-form::attr(data-price)').get().replace('$', '').replace(',', '')
                                break
                        else:
                            # We looked at all in-stock conditions for the card
                            # and none of the conditions matched our condition.
                            # The card/condition we want is out of stock.
                            price_model['qty_in_stock'] = 0
                            price_model['price'] = None

                    price_model['timestamp'] = datetime.datetime.now(datetime.timezone.utc)
                    yield price_model

                    # # WRITE TO FILE
                    # with open('thing.txt', 'a') as f:
                    #     f.write(str(price_model.__dict__))
                    #     f.write('\n')
                except:
                    # For whatever reason -- likely regex mismatch --
                    # the card_listing was not scraped. We log it in a text file
                    # for now. IMPROVE THIS so we can retry skipped cards!
                    with open('skipped.log', 'a') as f:
                        f.write(str(card_listing.css('h4.name::text').get() + '\t' + condition.name))
                        f.write('\n')

        # Go to next page if next page exists.
        next_page = response.css('a.next_page::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
