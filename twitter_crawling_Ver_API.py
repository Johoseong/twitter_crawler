import requests
import json
import time
import demoji
import ast
import re
from conf import config

class Crawling:
    bearer_token = ""
    search_url = ""
    query_params = {}
    fw_name = ""

    def __init__(self):
        # set BEARER_TOKEN in conf.py  ex) config = { 'bearer_token' : ... }
        self.bearer_token = config['bearer_token']
        self.search_url = "https://api.twitter.com/2/tweets/search/all"

        self.query_params = {'query': '', 'tweet.fields': 'created_at,lang,author_id,entities,geo',
                              'start_time': '', 'end_time': '', 'max_results': '500'}
        self.fw_name = ""

    def create_headers(self):
        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}
        return headers

    def connect_to_endpoint(self, headers):
        response = requests.request("GET", self.search_url, headers=headers, params=self.query_params)
        # print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def make_file_name(self, keyword):
        return keyword + self.query_params['start_time'][0:10] + "~" + self.query_params['end_time'][0:10]

    def main_act_indi(self, keyword_list, keyword, start_time, end_time):
        self.query_params['start_time'] = start_time
        self.query_params['end_time'] = end_time

        # main activity
        self.fw_name = 'output/' + self.make_file_name(keyword) + ".txt"
        fw = open(self.fw_name, "w", encoding="UTF8") # illegal multibyte sequence 오류 -> UTF8 설정으로 고침

        for keyword in keyword_list:
            self.query_params['query'] = keyword
            print(self.query_params)
            self.crawling_part(fw)

    ''' start crawling 
     parameter : 크롤링 결과가 담길 파일 객체 '''
    def crawling_part(self, fw):
        headers = self.create_headers()

        # crawling 후 json_response에 twit 데이터 저장 
        json_response = self.connect_to_endpoint(headers)
        ## twit text 문장 안에 '/" 있을 시 json으로 파싱 에러 -> 제거해줌
        for i in range(0, len(json_response['data'])):
            json_response['data'][i]['text'] = json_response['data'][i]['text'].replace("'", "").replace('"', "")

        # 이모티콘/느낌표,물음표 제거 (이모티콘 제거 안할 시 -> encoding 에러 발생)
        json_response = str(json_response)
        json_response = demoji.replace(json_response, '')
        # json_response = re.sub(r'[^ 0-9ㄱ-ㅣ가-힣A-Za-z.,!?"\':;~_\-@(){}\[\]]', '', json_response)
        json_response = re.sub(r'[^ 0-9ㄱ-ㅣ가-힣A-Za-z.,=<>+^$%&!?"\':;~_\-@(){}\[\]]', '', json_response)
        json_response = ast.literal_eval(json_response)
        
        for i in range(json_response["meta"]["result_count"]):
            json_response["data"][i]["text"] = re.sub("n", '', json_response["data"][i]["text"])  # 줄바꿈 n 쓰레기값 제거
            " ".join(json_response["data"][i]["text"].split())

            if ("entities" not in json_response["data"][i]):
                continue
            if ("hashtags" not in json_response["data"][i]["entities"]):
                del json_response["data"][i]["entities"]
                continue
            
            hashtags = []
            for h in json_response["data"][i]["entities"]["hashtags"]:
                hashtags.append(h["tag"])

            json_response["data"][i]["hashtags"] = hashtags
            del json_response["data"][i]["entities"]

        # json 파싱
        data = json.dumps(json_response, indent=4, sort_keys=True)
        data = data.encode('utf-8')

        # 한글 출력 위한 decode
        data = data.decode('unicode_escape', 'replace')

        fw.write(data)
        try:
            self.query_params['next_token'] = json_response['meta']['next_token']
        except Exception as e:
            print(self.query_params['query'] + " done")
            self.query_params['next_token'] = "DUMMY"
            del self.query_params['next_token']
            # print(e)
            time.sleep(3)
            return
        time.sleep(3)
        self.crawling_part(fw)