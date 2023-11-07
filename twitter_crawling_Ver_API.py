import requests
import json
import time
import demoji
import ast
import re

class Crawling:
    bearer_token = ""
    search_url = ""
    query_params = {}
    fw_name = ""

    def __init__(self):
        # To set your environment variables in your terminal run the following line:
        # export 'BEARER_TOKEN'='<your_bearer_token>'
        self.bearer_token = ""
        self.search_url = "https://api.twitter.com/2/tweets/search/all"
        self.search_url_from_id = "https://api.twitter.com/2/users/"

        # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
        # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
        self.query_params = {'query': '',
                              'start_time': '2016-01-01T00:00:00Z', 'end_time': '2021-01-01T00:00:00Z', 'max_results': '10'}
        # self.query_params = {'query': '', 'tweet.fields': 'created_at,lang,author_id',
        #                       'start_time': '2016-01-01T00:00:00Z', 'end_time': '2021-01-01T00:00:00Z', 'max_results': '10'} 
        self.query_params_id = {'tweet.fields': 'created_at,lang,author_id,geo', 'start_time': '2016-01-01T00:00:00Z', 'end_time': '2021-01-01T00:00:00Z',
                                'max_results': '100'}
        # expansions=author_id&tweet.fields=created_at,author_id,conversation_id,public_metrics,context_annotations&user.fields=username&max_results=5
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

    def main_act_indi(self, brand_list, drug_name, start_time, end_time):
        self.query_params['start_time'] = start_time
        self.query_params['end_time'] = end_time
        # self.query_params['tweet.fields'] = "lang,created_at,author_id"
        # self.query_params['expansions'] = "geo.place_id"
        # self.query_params['place.fields'] = "country"

        # main activity
        # self.fw_name = drug_name + " " + self.query_params['start_time'][0:10] + "~" + self.query_params['end_time'][0:10] + ".txt"
        self.fw_name = 'output/' + drug_name + ''.join(self.query_params['start_time'].split('-')[0:2]) + ".txt"
        fw = open(self.fw_name, "w", encoding="UTF8") # illegal multibyte sequence 오류 -> UTF8 설정으로 고침
        for brand_name in brand_list:
            self.query_params['query'] = brand_name
            print(self.query_params)
            self.crawling_part(fw)

    ''' start crawling 
     parameter : 크롤링 결과가 담길 json 파일 객체 '''
    def crawling_part(self, fw):
        headers = self.create_headers()

        # crawling 후 json_response에 twit 데이터 저장 
        json_response = self.connect_to_endpoint(headers)
        ## twit text 문장 안에 '/" 있을 시 json으로 파싱 에러 -> 제거해줌
        for i in range(0, len(json_response['data'])):
            json_response['data'][i]['text'] = json_response['data'][i]['text'].replace("'", "").replace('"', "")

        # 이모티콘/느낌표,물음표 제거 (이모티콘 제거 안할 시 -> encoding 에러 발생)
        json_response = str(json_response)
        # json_response = emoji.get_emoji_regexp().sub(r'', json_response)
        json_response = demoji.replace(json_response, '')
        # json_response = re.sub(r'[^ 0-9ㄱ-ㅣ가-힣A-Za-z.,!?"\':;~_\-@(){}\[\]]', '', json_response)
        json_response = re.sub(r'[^ 0-9ㄱ-ㅣ가-힣A-Za-z.,=<>+^$%&!?"\':;~_\-@(){}\[\]]', '', json_response)
        json_response = ast.literal_eval(json_response)
        # print(json_response["meta"]["result_count"])
        for i in range(json_response["meta"]["result_count"]):
            json_response["data"][i]["text"] = re.sub("n", '', json_response["data"][i]["text"])
            " ".join(json_response["data"][i]["text"].split())

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