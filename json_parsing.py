import json
import ast
import os

class Parsing:
    path = ""
    input_name = ""
    output_name = ""
    keyword = ""

    def __init__(self, input, keyword):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/"
        self.input_name = input
        self.keyword = keyword

    def counting(self, dummy):
        i = 0
        RB = True
        while(RB):
            try:
                dummy['data'][i]['text']
                i = i+1
            except IndexError:
                mo_cnt = i
                RB = False

        return mo_cnt

    def json_parse(self, f, keyword, author_id, twit_id, lang, tag, date, time, org_twit, geo_id, retwit_acct, hashtags):
        datas = {
                "keyword": keyword,
                "author_id": author_id,
                "twit_id": twit_id,
                "lang": lang,
                "tag": tag,
                "date": date,
                "time": time,
                "twit": org_twit,
                "geo_id": geo_id,
                "retwit_acct": retwit_acct,
                "hashtags": hashtags
                }
        final_d.append(datas)

    def main_parsing(self):
        self.output_name = self.input_name.split('.')[0] + ".json"
        input_file = open(self.path + self.input_name, "r", encoding="UTF8")
        f = open(self.path + self.output_name, "w", encoding="UTF8")
        
        text = input_file.readlines()

        mo_cnt = 0 
        global final_d
        final_d = list()
        final_s = 0

        start = 0
        for line in text:
            if '"data"' in line:
                dummy = "{"
                start = 1
            if '"result_count"' in line:
                start = 0
                dummy += "}}"
                dummy = ast.literal_eval(dummy)
                
                mo_cnt = self.counting(dummy)
                print(mo_cnt)

                # news_keyword = ['뉴스', '일보', '출처', '신문', '기자']

                for i in range(mo_cnt):
                    checking = dummy['data'][i]['text']
                    sp_ch = checking.split(" @")
                    geo = ""
                    # is_news = 0

                    # for j in news_keyword:
                    #     if j in checking:
                    #         is_news = 1
                    # if is_news == 1:
                    #     continue
                            
                    if "geo" in dummy['data'][i]:
                        geo = dummy['data'][i]['geo']['place_id']

                    if len(sp_ch) > 2:
                        sp_ch[1] = sp_ch[1] + " @" + sp_ch.pop(-1)

                    if (sp_ch[0] == 'RT'):
                        sp_ch = sp_ch[1].split(":")
                        sp_id = sp_ch.pop(0)
                        tag_flag = 1
                        checking = "".join(sp_ch).strip()
                    else:
                        sp_id = ""
                        tag_flag = 0
                    
                    keyword = self.keyword
                    author_id = dummy['data'][i]['author_id']
                    twit_id = dummy['data'][i]['id']
                    lang = dummy['data'][i]['lang']
                    tag = tag_flag # retwit
                    sp_d = dummy['data'][i]['created_at'].split("T")
                    date = sp_d[0]
                    time = sp_d[1].replace("Z", "")
                    org_twit = checking
                    geo_id = geo
                    retwit_acct = sp_id
                    hashtags = []
                    if ("hashtags" in dummy['data'][i]):
                        hashtags = dummy['data'][i]['hashtags']

                    self.json_parse(f, keyword, author_id, twit_id, lang, tag, date, time, org_twit, geo_id, retwit_acct, hashtags)

        
                final_s = json.dumps(final_d, indent ='\t', ensure_ascii=False)
                
            if start == 1:
                dummy += line

        f.write(final_s)