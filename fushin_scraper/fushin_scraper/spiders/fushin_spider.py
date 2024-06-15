import scrapy
import requests

class FushinSpider(scrapy.Spider):
    name = "fushin_spider"
    allowed_domains = ["fushinsha-joho.co.jp"]
    start_urls = ["https://fushinsha-joho.co.jp/"]
    DEBUG = True
    DEBUG_NUM_YM = 3 # デバッグモードで取得する年月ページの数
    DEBUG_NUM_ARTICLE = 3 # デバッグモードで取得する一つの年月あたりの記事数
    
    def parse_ym(self, response):
        '''年月ページにおける個別記事の見出し・URLを取得.URLからhtmlを取得しタイトルと日付を取得'''
        post_list = [post for post in response.css('li')]

        if self.DEBUG:
            post_list = post_list[:self.DEBUG_NUM_ARTICLE]
        for post in post_list:
            # 月別ページで表示される個別記事の見出し・URLを取得
            _url = post.css('a::attr(href)').extract_first().strip()
            _title = post.css('a::text').extract_first().strip()

            # 個別記事の情報を取得
            if _url is not None:
                response_detail = requests.get(_url, verify = False)
                response_detail = scrapy.http.TextResponse(body = response_detail.content, url = _url)
                _title_detail = response_detail.css('h1::text').extract_first().strip()
                _date = response_detail.css('label.articleDate__date>bdi::text').extract_first().strip()

                result = dict(date = _date, title = _title, title_detail = _title_detail, url = _url)
                yield result

    def parse(self, response):
        '''トップページのドロップダウンから年月ページのURLのリストを作成しURLをparse_ymに渡す'''
        ym_list = response.xpath('//select[@id="ym_select"]/option/@value').extract()
        ym_url_list = ['https://fushinsha-joho.co.jp/?ym=' + ym for ym in ym_list]
        if self.DEBUG:
            ym_url_list = ym_url_list[:self.DEBUG_NUM_YM]
        for ym_url in ym_url_list:
            if ym_url is not None:
                yield scrapy.Request(ym_url, callback=self.parse_ym)
