# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
import datetime

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']
    n = 0

    def parse(self, response):
        '''
        1.获取文章列表中的文章url、下载、解析
        2.获取下一页的url、下载后交给parse函数
        '''

        # 1.获取文章列表中的文章url、下载、解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            JobboleSpider.n += 1
            print(JobboleSpider.n)
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': image_url}, callback=self.parse_detail)

        # 2.获取下一页的url、下载后交给parse函数
        next_url = response.css(".next.page-numbers::attr(href)").extract_first('')
        print('next_url'+ next_url)
        if next_url:
            url=parse.urljoin(response.url, next_url)
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):

        article_item = JobBoleArticleItem()
        # 提取文章具体字段

        # /html/body/div[3]/div[3]/div[1]/div[1]
        # // *[ @ id="post-113737"] / div[1] / h1
        # re_selector = response.xpath('/html/body/div[1]/div[3]/div[1]/div[1]/h1')
        # re2_selector=response.xpath('//*[@id="post-113737"]/div[1]/h1/text()')
        # re3_selector=response.xpath('//div[@class="entry-header"]/h1/text()')

        # 标题、日期
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace('·','').strip()
        # # 点赞数、收藏数、评论数
        # prase_nums = int(response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0])
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # match_re = re.match('.*?(\d+).*', fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        # comments_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re=re.match('.*?(\d+).*', comments_nums)
        # if match_re:
        #     comments_nums = int(match_re.group(1))
        # else:
        #     comments_nums = 0
        # # 内容
        # content = response.xpath("//div[@class='entry']").extract()[0]
        # # 标签
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ','.join(tag_list)

        # 通过css选择器提取字段
        # front_image_url = response.meta.get('front_image_url', '')  # 文章封面图
        # title = response.css(".entry-header h1::text").extract()[0]
        # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace('·','').strip()
        # try:
        #     create_date = datetime.datetime.strptime(create_date, '%Y%m%d').date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # prase_nums = response.css(".vote-post-up h10::text").extract()[0]
        # fav_nums = response.css(".bookmark-btn::text").extract()[0]
        # match_re=re.match('.*?(\d+).*', fav_nums)
        # if match_re:
        #     fav_nums= int(match_re.group(1))
        # else:
        #     fav_nums=0
        # comments_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        # match_re=re.match('.*?(\d+).*', comments_nums)
        # if match_re:
        #     comments_nums = int(match_re.group(1))
        # else:
        #     comments_nums=0
        # content = response.css("div.entry").extract()[0]
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        # tag_list=[element for element in tag_list if not element.strip().endswith("评论")]
        # tags=','.join(tag_list)
        #
        # article_item['title'] = title
        # article_item['url'] = response.url
        # article_item['url_object_id'] = get_md5(response.url)
        # article_item['create_date'] = create_date
        # article_item['front_image_url'] = [front_image_url]
        # article_item['prase_nums'] = prase_nums
        # article_item['fav_nums'] = fav_nums
        # article_item['comments_nums'] = comments_nums
        # article_item['content'] = content
        # article_item['tags'] = tags
        # # front_image_path在pipelines.py中填充

        # 通过ItemLoader加载item
        front_image_url = response.meta.get('front_image_url', '')  # 文章封面图
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('create_date', 'p.entry-meta-hide-on-mobile::text')
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_css('prase_nums', '.vote-post-up h10::text')
        item_loader.add_css('fav_nums', '.bookmark-btn::text')
        item_loader.add_css('comments_nums', "a[href='#article-comment'] span::text")
        item_loader.add_css('content', 'div.entry')

        article_item = item_loader.load_item()


        yield article_item
