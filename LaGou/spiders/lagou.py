# -*- coding: utf-8 -*-
import scrapy
from LaGou.items import LagouItem
import json
from pprint import pprint
import time


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/list_python?']

    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Connection": "keep-alive",
            "Host": "www.lagou.com",
            "Referer": 'https://www.lagou.com/jobs/list_Python?px=default&city=%E6%AD%A6%E6%B1%89',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "referer": "https://www.lagou.com/jobs/list_python?"
        }
        self.sid = ''
        self.job_url_temp = 'https://www.lagou.com/jobs/{}.html?show={}'
        # 清空文件
        with open('jobs.json', 'w') as f:
            f.truncate()

    def parse(self, response):
        """
        解析起始页
        """
        # response为GET请求的起始页, 自动获取cookie
        # 提交POST带上前面返回的cookies, 访问数据结果第一页
        yield scrapy.FormRequest(
            'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',
            callback=self.parse_list,
            formdata={"first": "false",
                      "pn": "1",
                      "kd": "python",
                      },
            headers=self.headers
        )
    def parse_list(self, response):
        """
        解析结果列表页的json数据
        """
        # 获取返回的json,转为字典
        res_dict = json.loads(response.text)
        # 判断返回是否成功
        if not res_dict.get('success'):
            print(res_dict.get('msg', '返回异常'))
        else:
            # 获取当前页数
            page_num = res_dict['content']['pageNo']
            print('正在爬取第{}页'.format(page_num))
            # 获取sid
            if not self.sid:
                self.sid = res_dict['content']['showId']
            # 获取响应中的职位url字典
            part_url_dict = res_dict['content']['hrInfoMap']
            # 遍历职位字典
            for key in part_url_dict:
                # 初始化保存职位的item
                item = LagouItem()
                # 拼接完整职位url
                item['job_url'] = self.job_url_temp.format(key, self.sid)
                # 请求职位详情页
                yield scrapy.Request(
                    item['job_url'],
                    callback=self.parse_detail,
                    headers=self.headers,
                    meta={'item': item}
                )

            # 获取下一页
            if page_num < 30:
                # time.sleep(2)
                yield scrapy.FormRequest(
                    'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',
                    callback=self.parse_list,
                    formdata={"first": "false",
                              "pn": str(page_num+1),
                              "kd": "python",
                              "sid": self.sid
                             },
                    headers=self.headers
                )

    def parse_detail(self, response):
        """
        解析职位详情页
        """
        # 接收item
        item = response.meta['item']
        # 解析数据
        # 获取职位头div
        job_div = response.xpath('//div[@class="position-content-l"]')
        if job_div:
            item['job_name'] = job_div.xpath('./div/h1/text()').extract_first()
            item['salary'] = job_div.xpath('./dd/h3/span[1]/text()').extract_first().strip()
            item['city'] = job_div.xpath('./dd/h3/span[2]/text()').extract_first().strip('/').strip()
            item['area'] = response.xpath('//div[@class="work_addr"]/a[2]/text()').extract_first()
            item['experience'] = job_div.xpath('./dd/h3/span[3]/text()').extract_first().strip('/').strip()
            item['education'] = job_div.xpath('./dd/h3/span[4]/text()').extract_first().strip('/').strip()
            item['labels'] = response.xpath('//ul[@class="position-label clearfix"]/li/text()').extract()
            item['publish_date'] = response.xpath('//p[@class="publish_time"]/text()').extract_first()
            item['publish_date'] = item['publish_date'].split('&')[0]
            # 获取公司dl
            company_div = response.xpath('//dl[@class="job_company"]')
            item['company'] = company_div.xpath('./dt/a/img/@alt').extract_first()
            item['company_feature'] = company_div.xpath('./dd//li[1]/h4[@class="c_feature_name"]/text()').extract_first()
            item['company_feature'] = item['company_feature'].split(',')
            item['company_public'] = company_div.xpath('./dd//li[2]/h4[@class="c_feature_name"]/text()').extract_first()
            item['company_size'] = company_div.xpath('./dd//li[4]/h4[@class="c_feature_name"]/text()').extract_first()
            yield item

