import csv
import datetime
import json
import os
import requests
from loguru import logger


class Twitter:
    def __init__(self, cookie, authorization, token):
        # self.proxy = {
        #      'http': 'http://127.0.0.1:10090',
        #      'https': 'http://127.0.0.1:10090',
        #  }
        self.proxy = None
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        self.headers = {
            "authority": "twitter.com",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
            "authorization": authorization,
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
            "cookie": cookie,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.ua,
            "x-csrf-token": token,
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en"
        }

    def req(self, url, params=None, data=None):
        for i in range(5):
            try:
                if not data:
                    return requests.get(url, headers=self.headers, params=params, timeout=10, proxies=self.proxy)
                return requests.post(url, headers=self.headers, params=params, data=data, timeout=10,
                                     proxies=self.proxy)
            except Exception as e:
                logger.error(e)

    def search(self, raw_query, cursor):
        url = "https://twitter.com/i/api/graphql/NA567V_8AFwu0cZEkAAKcw/SearchTimeline"
        params = {
            "variables": json.dumps({
                "rawQuery": raw_query,
                "count": 20,
                "cursor": cursor,
                "querySource": "typed_query",
                "product": "Top"
            }),
            "features": "{\"rweb_lists_timeline_redesign_enabled\":true,\"responsive_web_graphql_exclude_directive_enabled\":true,\"verified_phone_label_enabled\":false,\"creator_subscriptions_tweet_preview_api_enabled\":true,\"responsive_web_graphql_timeline_navigation_enabled\":true,\"responsive_web_graphql_skip_user_profile_image_extensions_enabled\":false,\"tweetypie_unmention_optimization_enabled\":true,\"responsive_web_edit_tweet_api_enabled\":true,\"graphql_is_translatable_rweb_tweet_is_translatable_enabled\":true,\"view_counts_everywhere_api_enabled\":true,\"longform_notetweets_consumption_enabled\":true,\"responsive_web_twitter_article_tweet_consumption_enabled\":false,\"tweet_awards_web_tipping_enabled\":false,\"freedom_of_speech_not_reach_fetch_enabled\":true,\"standardized_nudges_misinfo\":true,\"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled\":true,\"longform_notetweets_rich_text_read_enabled\":true,\"longform_notetweets_inline_media_enabled\":true,\"responsive_web_media_download_video_enabled\":false,\"responsive_web_enhance_cards_enabled\":false}"
        }
        response = self.req(url, params=params).json()
        return response["data"]["search_by_raw_query"]["search_timeline"]["timeline"]["instructions"]

    def search_run(self, keyword, data_num, csv_file=None):
        cursor = ''
        tt = []
        while len(tt) < data_num:
            out_data = []
            logger.info(f"[搜索推文] {keyword} {cursor}")
            instructions = self.search(keyword, cursor)
            if not instructions[0].get('entries'):
                logger.warning(f"[搜索推文] 无数据 {keyword} {cursor}")
                break
            for entry in instructions[0].get('entries'):
                if not self.is_tweet_entry(entry):
                    continue
                tweet_results = self.get_tweet_results(entry)
                tweet_results = tweet_results['tweet'] if tweet_results.get('tweet') else tweet_results
                legacy = tweet_results['legacy']
                user_legacy = tweet_results["core"]["user_results"]["result"]["legacy"]
                item = {
                    '搜索关键字': keyword,
                    '推文id': tweet_results['rest_id'],
                    '推文文本': tweet_results["legacy"]["full_text"],
                    '推文地址': f'https://twitter.com/PeerAmeerAShah/status/{tweet_results["rest_id"]}',
                    '发布时间': datetime.datetime.strptime(legacy['created_at'], "%a %b %d %H:%M:%S %z %Y"),
                    '播放量': tweet_results['views'].get('count'),
                    '点赞数': legacy['favorite_count'],
                    '评论数': legacy['reply_count'],
                    '转推数': legacy['retweet_count'],
                    '发布人昵称': user_legacy['screen_name'],
                    '发布人主页链接': "https://twitter.com/" + user_legacy['screen_name'],
                    '发布人简介': user_legacy['description'],
                    '发布人加入时间': datetime.datetime.strptime(user_legacy['created_at'],
                                                                   "%a %b %d %H:%M:%S %z %Y"),
                    '发布人粉丝数': user_legacy['followers_count'],
                    '发布人关注数': user_legacy['friends_count'],
                    '发布人作品数': user_legacy['media_count']
                }
                print(item)
                self.get_user_info_by_entry(tweet_results, item)
                out_data.append(item)
                tt.append(item)
            if csv_file:
                self.write(out_data, csv_file)
            cursor = self.get_cursor(instructions)
            if not cursor:
                break
        return tt

    @staticmethod
    def get_tweet_results(entry):
        if entry['content'].get('items'):
            result = entry['content']['items'][0]['item']['itemContent']['tweet_results']['result']
            if result.get('legacy'):
                return result
            return entry['content']['items'][-1]['item']['itemContent']['tweet_results']['result']
        return entry["content"]["itemContent"]["tweet_results"]["result"]

    def get_user_info_by_entry(self, tweet_results, item):
        user_legacy = tweet_results["core"]["user_results"]["result"]["legacy"]
        item['评论用户昵称'] = user_legacy['screen_name']
        item['评论用户主页链接'] = "https://twitter.com/" + user_legacy['screen_name']
        item['评论用户简介'] = user_legacy['description']
        item['评论用户加入时间'] = datetime.datetime.strptime(user_legacy['created_at'], "%a %b %d %H:%M:%S %z %Y")
        item['评论用户粉丝数'] = user_legacy['followers_count']
        item['评论用户关注数'] = user_legacy['friends_count']
        item['评论用户作品数'] = user_legacy['media_count']

    @staticmethod
    def is_tweet_entry(entry):
        return entry['entryId'].startswith('tweet-')

    @staticmethod
    def get_cursor(instructions):
        if instructions[0].get('entries') and 'cursor-bottom' in instructions[0].get('entries')[-1]['entryId']:
            entries = instructions[0].get('entries')
            if entries[-1]['content'].get('itemContent'):
                return entries[-1]['content']['itemContent']['value']
            return entries[-1]['content']['value']
        elif instructions[-1].get('entry') and 'cursor-bottom' in instructions[-1]['entry']['entryId']:
            return instructions[-1]['entry']['content']['value']
        return ''

    @staticmethod
    def write(data, path):
        if data:
            with open(path + '.csv', 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerows(data)

    @staticmethod
    def r_write(data, path):
        if data:
            with open(path + '.csv', 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerows(data)

    @staticmethod
    def read_csv(path) -> [dict]:
        if not os.path.exists(path + '.csv'):
            return []
        data: [dict] = []
        with open(path + '.csv', 'r', newline='', encoding='utf-8-sig') as f:
            for d in csv.DictReader(f):
                data.append(d)
        return data


cookie = 'guest_id=v1%3A171965722395363503; night_mode=2; guest_id_marketing=v1%3A171965722395363503; guest_id_ads=v1%3A171965722395363503; gt=1806999761268150550; g_state={"i_p":1719664482691,"i_l":1}; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; kdt=ofi2SnazSRWn4PX6ANlp3TXDsumaalUo5s99meSS; auth_token=4d5e15a02e6d6b585d34fbcb552a47d1bd6e89ba; ct0=fe8b1ff3bd7b631e7e879d859310776a0eb9756bf7b88be618db87db3fa6c0aee072107217594aed9e21a425cc9938e0d159a09a87ba6d9b815d58555666b7201d9b0a52c21414d67a0ab08fcccdfe94; att=1-8jcFmsagqvdf3FM7Xqx2T72WPElsg1hd3JAWvjiK; lang=en; twid=u%3D1752712903671627776; personalization_id="v1_n9lFsHC8eW+u6VdJPJaZIA=="'
authorization = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
token = 'fe8b1ff3bd7b631e7e879d859310776a0eb9756bf7b88be618db87db3fa6c0aee072107217594aed9e21a425cc9938e0d159a09a87ba6d9b815d58555666b7201d9b0a52c21414d67a0ab08fcccdfe94'
# 搜索关键字
keyword = 'election fake news'
# 保存多少条数据
data_num = 100
# 保存文件的名字
save_file_name = keyword

twitter = Twitter(cookie, authorization, token)
twitter.search_run(keyword, data_num, save_file_name)
