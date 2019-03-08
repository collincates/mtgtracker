import re
import scrapy
from price.models import Card, Condition, Vendor
from scraper.scraper.items import PriceItem

import datetime


class CFBSpider(scrapy.Spider):
    name= 'cfb_spider'
    start_urls = [
        # 'https://store.channelfireball.com/catalog/magic_singles-old_expansions-fallen_empires/60'
        'https://store.channelfireball.com/catalog/magic_singles-old_expansions-arabian_nights/64'
        # 'https://store.channelfireball.com/catalog/magic_singles-old_expansions-antiquities/63'
    ]
    # def start_requests(self):
    #     """
    #     Open urls.list and create a Request object for each one.
    #     Use a context manager here to avoid hard-coding URLs.
    #     """
    #     with open('urls.list', 'r') as f:
    #         for url in f.readlines():
    #             yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        main_regex_sub_pattern = '[^0-9a-zA-Z ]'

        expansion_name = response.css(
            "meta.site-settings::attr(data-category)"
            ).get()

        # Get all Card objects from the set that we're currently working with,
        # sorted by card name. We need to sort here in order to make ensure that
        # the sorted regex patterns we are about to make will correspond to the
        # correct card object once we zip (Card, pattern) tuples in a moment.
        #
        # Store these sorted Card objects in a tuple.
        #
        # TODO:
        # 'set_name__contains' will find all sets that have the scraped
        # word in them. How to deal with words that appear
        # in multiple sets? An example of this is scraping the word
        # 'Ravnica' and knowing there are sets called 'Ravnica',
        # 'Return to Ravnica', 'Ravnica Allegiance', and maybe others
        # planned for the future.
        # 'set_name__contains' will return a single object in the case
        # that there is only one set with this scraped name in it.
        # In the example above, however, a Queryset of multiple sets
        # will be returned. Figure this out!
        card_objects_from_db = tuple(
            Card.objects.filter(
                set_name__contains=f'{expansion_name}').order_by('name').all()
        )

        # Create regex patterns from the database string representations of card
        # names, which can sometimes include non-alphanumeric characters that
        # we want to replace with the regex '.' as in "any one character".
        #
        #       Actual string:          Converted regex pattern
        #       --------------          -----------------------
        #       'Dandân'                '^Dand.n$'
        #       'El-Hajjâj'             '^El.Hajj.j$'
        #       'Ring of Ma'rûf'        '^Ring of Ma.r.f$'
        #
        # The variable card_name_regex_patterns is a tuple of these patterns,
        # one for each Card object in card_objects_from_db, stored in the same
        # sort order as the Card objects.

        card_name_regex_patterns = tuple([
            str('^' + re.sub(main_regex_sub_pattern, '.', card.name, flags=re.ASCII) + '$') \
            for card in card_objects_from_db
        ])

        # Now, zip each Card object and its corresponding regex pattern into
        # a tuple. Store these tuples in a tuple!
        card_name_tuples = tuple(zip(
            card_objects_from_db,
            card_name_regex_patterns
        ))

        cfb_card_list = response.css('li.product')
        cfb_conditions = Vendor.objects.get(code='CFB').conditions.all()
        cfb_vendor_object = Vendor.objects.get(code='CFB')

        for card_listing in cfb_card_list:
            for condition in cfb_conditions:
                try:
                    price_model = PriceItem()
                    # split_title is a tuple of one or more regex capture groups.
                    # Right now, split_title may or may not contain data beyond
                    # the first capture group. If it does, this can be used to
                    # determine the artist name, or other aspencts about the
                    # card's visual details.
                    split_title = tuple(filter(
                        None,
                        re.split(
                            '^(.+)(?=\\ \\() \((.+)\)$',
                            card_listing.css('h4.name::text').get()
                        )
                    ))
                    # As with above, we apply a regex subsitution in order to
                    # replace all non-alphanumeric with '.' which builds a new
                    # regex pattern where any non-alphanumeric character can
                    # now represent any single character.
                    # This allows for 'û' to refer to 'u', regexically(?), and
                    # provides a dynamic solution for the various ways that
                    # card and artist names are represented across Magic.
                    cleaned_cfb_card_name = re.sub(main_regex_sub_pattern, '.', split_title[0], flags=re.ASCII)

                    # Compare the database's card name regex pattern with the
                    # cleaned_cfb_card_name
                    price_model['card'] = [card_name_tuple[0] for card_name_tuple in card_name_tuples if re.match(card_name_tuple[1], cleaned_cfb_card_name)][0]
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

                except:
                    # TODO:
                    # If for whatever reason -- likely regex mismatch --
                    # the card_listing was not scraped. We log it in a file
                    # for now. IMPROVE THIS so we can retry skipped cards!
                    with open('skipped.log', 'a') as f:
                        f.write(card_listing + '\t' + condition)
                        f.write('\n')

        # Go to next page if next page exists.
        next_page = response.css('a.next_page::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
