import json
import ast
import os
import re

class Parsing:
    path = ""
    input_name = ""
    output_name = ""
    mo_str = ""
    eng_str = ""

    def __init__(self, input, eng_keyword):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/"
        self.input_name = input
        self.eng_str = eng_keyword
        # self.output_name = self.input_name.split('.')[0] + " parsed.json"

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

    # def json_not_re(self, f, keyword, eng_keyword, author_id,twit_id,lang,tag,date,time,org_twit,geo_id,hash_i, retwit_acct, refined_twit):
    #     datas = {
    #             "keyword": keyword,
    #             "eng_keyword": eng_keyword,
    #             "author_id": author_id,
    #             "twit_id": twit_id,
    #             "lang": lang,
    #             "tag": tag,
    #             "date": date,
    #             "time": time,
    #             "org_twit": org_twit,
    #             "geo_id": geo_id,
    #             "hash": "...",
    #             "retwit_acct": retwit_acct,
    #             "refined_twit": refined_twit
    #             }
    #     final_d.append(datas)

    # def json_re(self, f, keyword, eng_keyword, author_id,twit_id,lang,tag,date,time,org_twit,geo_id,hash_i,retwit_acct,refined_twit):
    #     datas = {
    #             "keyword": keyword,
    #             "eng_keyword": eng_keyword,
    #             "author_id": author_id,
    #             "twit_id": twit_id,
    #             "lang": lang,
    #             "tag": tag,
    #             "date": date,
    #             "time": time,
    #             "org_twit": org_twit,
    #             "geo_id": geo_id,
    #             "hash": "...",
    #             "retwit_acct": retwit_acct,
    #             "refined_twit": refined_twit
    #             }
    #     final_d.append(datas)

    def json_parse(self, f, keyword, eng_keyword, author_id,twit_id,lang,tag,date,time,org_twit,geo_id,hash_i,retwit_acct):
        datas = {
                "keyword": keyword,
                "eng_keyword": eng_keyword,
                "author_id": author_id,
                "twit_id": twit_id,
                "lang": lang,
                "tag": tag,
                "date": date,
                "time": time,
                "twit": org_twit,
                "geo_id": geo_id,
                "hash": "...",
                "retwit_acct": retwit_acct,
                }
        final_d.append(datas)

    def main_parsing(self):
        self.output_name = self.input_name.split('.')[0] + ".json"
        input_file = open(self.path + self.input_name, "r", encoding="UTF8")
        f = open(self.path + self.output_name, "w", encoding="UTF8")
        
        text = input_file.readlines()

        mo_cnt = 0
        mo_str = self.input_name.split('.')[0:-6]   
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
                    
                    keyword = mo_str
                    eng_keyword = self.eng_str
                    author_id = dummy['data'][i]['author_id']
                    twit_id = dummy['data'][i]['id']
                    lang = dummy['data'][i]['lang']
                    tag = tag_flag # retwit
                    sp_d = dummy['data'][i]['created_at'].split("T")
                    date = sp_d[0]
                    time = sp_d[1].replace("Z", "")
                    org_twit = checking
                    geo_id = geo
                    hash_i = "..."
                    retwit_acct = sp_id

                    self.json_parse(f, keyword, eng_keyword, author_id, twit_id, lang, tag, date, time, org_twit, geo_id, hash_i, retwit_acct)

                    # if(sp_ch[0] == 'RT'):
                    #     sp_ch = sp_ch[1].split(":")
                        
                    #     sp_id = sp_ch.pop(0) # sp_id에 리트윗 원작자 아이디 들어감
                    #     # rt_remove_txt = "".join(sp_ch)
                    #     # rt_remove_txt = rt_remove_txt.strip()

                    #     # rt_remove_token = rt_remove_txt.split(" ")

                    #     # search = "https"
                    #     # for word in rt_remove_token:
                    #     #     if search in word: 
                    #     #         rt_remove_token.remove(word)
                    #     # url_remove_txt = " ".join(rt_remove_token)

                    #     # url_remove_txt = re.sub(r'[^ 0-9ㄱ-ㅣ가-힣]', ' ', url_remove_txt)
                    #     # url_remove_txt = " ".join(url_remove_txt.split())

                    #     keyword = mo_str
                    #     eng_keyword = self.eng_str
                    #     author_id = dummy['data'][i]['author_id']
                    #     twit_id = dummy['data'][i]['id']
                    #     lang = dummy['data'][i]['lang']
                    #     tag = 1 # retwit
                    #     sp_d = dummy['data'][i]['created_at'].split("T")
                    #     date = sp_d[0]
                    #     time = sp_d[1].replace("Z", "")
                    #     org_twit = checking
                    #     geo_id = geo
                    #     hash_i = "..."
                    #     retwit_acct = sp_id
                    #     # refined_twit = url_remove_txt

                    #     self.json_re(f, keyword, eng_keyword, author_id, twit_id, lang, tag, date, time, org_twit, geo_id, hash_i, retwit_acct, refined_twit)

                    # else:
                    #     checking = dummy['data'][i]['text']
                    #     # token = checking.split(" ")

                    #     # search = "https"
                    #     # for word in token:
                    #     #     if search in word: 
                    #     #         token.remove(word)
                    #     # url_remove_txt = " ".join(token)

                    #     # url_remove_txt = re.sub(r'[^ 0-9ㄱ-ㅣ가-힣]', ' ', url_remove_txt)
                    #     # url_remove_txt = " ".join(url_remove_txt.split())

                    #     keyword = mo_str
                    #     eng_keyword = self.eng_str
                    #     author_id = dummy['data'][i]['author_id']
                    #     twit_id = dummy['data'][i]['id']
                    #     lang = dummy['data'][i]['lang']
                    #     tag = 0 # not retwit
                    #     sp_d = dummy['data'][i]['created_at'].split("T")
                    #     date= sp_d[0]
                    #     time = sp_d[1].replace("Z", "")
                    #     org_twit = checking
                    #     geo_id = geo
                    #     hash_i = "..."
                    #     retwit_acct = ""
                    #     # refined_twit = url_remove_txt
                    #     self.json_not_re(f, keyword, eng_keyword, author_id, twit_id, lang, tag, date, time, org_twit, geo_id, hash_i, retwit_acct, refined_twit)
        
                final_s = json.dumps(final_d, indent ='\t')
                
            if start == 1:
                dummy += line

        final_s = final_s.encode('utf-8')
        final_s = final_s.decode('unicode_escape', 'replace')
        f.write(final_s)