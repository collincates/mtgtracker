from scrapy_djangoitem import DjangoItem
from price.models import Price

class PriceItem(DjangoItem):
    django_model = Price
