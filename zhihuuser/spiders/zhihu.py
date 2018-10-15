# -*- coding: utf-8 -*-
import scrapy
import json
from zhihuuser.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&amp;offset={offset}&amp;limit={limit}'
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&amp;offset={offset}&amp;limit={limit}'
    start_user = 'excited-vczh'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    
    def start_requests(self):
        # 用户基本信息
        yield scrapy.Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)
        # 关注列表
        yield scrapy.Request(
            self.follows_url.format(user=self.start_user, include=self.follows_query, limit=20, offset=0),
            self.parse_follows)
        # 粉丝列表
        yield scrapy.Request(
            self.followers_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=0),
            self.parse_followers)
    
    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        # print ('---666666---')
        # print (item)
        # print ('---777777---')
        # print (result)
        # print (result['url_token'])
        yield scrapy.Request(
            self.follows_url.format(user=result['url_token'], include=self.follows_query, limit=20, offset=0),
            self.parse_follows)
    
    def parse_follows(self, response):
        # print(response.text)
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results['data']:
                yield scrapy.Request(self.user_url.format(user=result['url_token'], include=self.user_query),
                                     self.parse_user)
        
        if 'paging' in results.keys() and results['paging']['is_end'] == False:
            next_page = results['paging']['next']
            yield scrapy.Request(next_page, self.parse_follows)
    
    def parse_followers(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results['data']:
                yield scrapy.Request(self.user_url.format(user=result['url_token'], include=self.user_query),
                                     self.parse_user)
        if 'paging' in results.keys() and results['paging']['is_end'] == False:
            next_page = results['paging']['next']
            yield scrapy.Request(next_page, self.parse_followers)
