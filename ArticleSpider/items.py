# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def date_convert(value):
    try:
        create_date=datetime.datetime.strptime(value, '%Y%m%d').date()
    except Exception as e:
        create_date=datetime.datetime.now().date()
    return create_date

def get_nums(value):
    match_re=re.match('.*?(\d+).*', value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums =0
    return nums

def remove_comment_tags(value):
    # 去掉tags中提取的评论
    if '评论' in value:
        return ''
    else:
        return value

def return_value(value):
    return value

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        input_processor = MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    prase_nums = scrapy.Field()
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comments_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor = MapCompose(remove_comment_tags),
        output_processor = Join(',')
    )

