# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from decimal import Decimal
from itemadapter.adapter import ItemAdapter
import re
import spacy
from scrapy.exceptions import NotConfigured, DropItem
nlp = spacy.load('de_core_news_md')

class DataCleaningPipeline:
    def process_item(self, item, spider):
        clean_description = re.sub('<.*?>', '', item['description'])
        item['description'] = clean_description.strip()
        return item

class FilterLocation:
    @classmethod
    def from_crawler(cls, crawler):

        # Access settings
        settings = crawler.settings

        # Get Settings of main area and sub area from settings.py
        main_area = settings.get('MAIN_AREA')
        sub_areas = settings.get('SUB_AREAS');

        # Raise NotConfigured if a required setting is missing
        if not main_area:
            raise NotConfigured

        if not sub_areas:
            raise NotConfigured

        return cls(main_area, sub_areas)

    def __init__(self, main_area, sub_areas):
        self.main_area = main_area
        self.sub_areas = sub_areas

    def is_outside_main_area(self,description):
        doc = nlp(description)
        for ent in doc.ents:
            if ent.label_ == 'LOC':
                if self.main_area in ent.text.lower() or self.is_subarea(ent.text.lower()):
                    return True
        return False

    def is_subarea(self,location):
        return location in self.sub_areas

    def process_item(self, item, spider):
        if self.main_area.lower() not in item['location'].lower():
            raise DropItem(f"Outside {self.main_area}:  {item['description']}")

        if self.main_area.lower() not in item['location'].lower():
            raise DropItem(f"Outside {self.main_area}:  {item['description']}")

        if self.is_outside_main_area(item['description']):
            raise DropItem(f"Outside {self.main_area}:  {item['location']}")
        return item


class FilterHouseProps:
    @classmethod
    def from_crawler(cls, crawler):

        # Access settings
        settings = crawler.settings

        # Get Settings of main area and sub area from settings.py
        grundstuck = settings.get('GRUNDSTUCK')
        zimmers = settings.get('ZIMMER');

        # Raise NotConfigured if a required setting is missing
        if not grundstuck:
            grundstuck = 0

        if not zimmers:
            zimmers = 0

        return cls(grundstuck, zimmers)

    def __init__(self, grundstuck, zimmers):
        self.grundstuck = grundstuck
        self.zimmers = zimmers

    def process_item(self, item, spider):
        if(item['zimmer_count'] != 0 and int(item['zimmer_count'])< self.zimmers):
            raise DropItem(f"Less than {self.zimmers} zimmers:  {item['location']}")

        if(item['grundstuck'] !=0.0 and Decimal(item['grundstuck'])< self.grundstuck):
            raise DropItem(f"Less than {self.grundstuck} grundstuck:  {item['location']}")

        return item
