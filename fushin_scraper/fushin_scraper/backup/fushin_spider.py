import scrapy
import requests

class FushinSpider(scrapy.Spider):
    name = "fushin_spider"
    allowed_domains = ["fushinsha-joho.co.jp"]
    start_urls = ["https://fushinsha-joho.co.jp/"]

    def parse_detail(self, response_detail):
        _title_detail = response_detail.css('h1::text').extract_first().strip()
        details = dict(title_detail = _title_detail)
        print('details:', details)
        return details

    def parse(self, response):
        DEBUG = True
        post_list = [post for post in response.css('li')]
        if DEBUG:
            post_list = post_list[:5]
        for post in post_list:
            # 月別ページの情報を取得
            _url = post.css('a::attr(href)').extract_first().strip()
            _title = post.css('a::text').extract_first().strip()

            # 詳細ページの情報を取得
            response_detail = requests.get(_url, verify = False)
            response_detail = scrapy.http.TextResponse(body = response_detail.content, url = _url)
            _title_detail = response_detail.css('h1::text').extract_first().strip()

            #コンテンツの並びが記事により違うためコンテンツ取得禁止
            #_contents, _, _situation, _facility = response_detail.css('p.ma__p::text').extract()
            #details = dict(title_detail = _title_detail, contents = _contents, situation = _situation, facility = _facility)
            result = dict(title = _title, title_detail = _title_detail, url = _url)
            yield result