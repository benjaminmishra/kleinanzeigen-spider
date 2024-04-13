# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from decimal import Decimal

def to_decimal(value):
    try:
        # Convert value to Decimal, handling any conversion errors
        return Decimal(value)
    except (TypeError, ValueError):
        # Handle or log the error as needed
        return None

def to_int(value):
    try:
        # Attempt to convert the value to an integer
        return int(value)
    except ValueError:
        # If conversion fails, return None or handle it as needed
        return None

class House(scrapy.Item):
    # define the fields for which data is being collected
    location = scrapy.Field()
    price = scrapy.Field()
    grundstuck = scrapy.Field(serializer=to_decimal)
    zimmer_count = scrapy.Field(serializer=to_int)
    description = scrapy.Field()
    link = scrapy.Field()
