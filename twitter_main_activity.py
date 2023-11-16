'''
커맨드 라인 실행법
argument: [시작날짜] [끝날짜] [키워드]
Ex) python twitter_main_activity.py 2021-05-01 2021-06-01 아스트라제네카,화이자
'''
import argparse
import twitter_crawling_Ver_API
import json_parsing

main_crawling = twitter_crawling_Ver_API.Crawling()

# main
def main(start_date, end_date, keyword_list):
    for i in range(0, len(keyword_list)):
        main_crawling.main_act_indi(keyword_list, keyword_list[i], start_date, end_date)

        file_name = main_crawling.fw_name 
        parsing = json_parsing.Parsing(file_name, keyword_list[i])
        parsing.main_parsing()

# argument parsing
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(nargs='+' ,help='Example) 2021-05-01', dest='start_date')
    parser.add_argument(nargs='+' ,help='Example) 2021-06-01', dest='end_date')
    parser.add_argument(nargs='+' ,help='Example) 아스트라제네카,화이자', dest='keyword')

    start = parser.parse_args().start_date
    end = parser.parse_args().end_date
    keyword = parser.parse_args().keyword

    start_date = start[0] + "T00:00:00Z"
    end_date = end[0] + "T00:00:00Z"
    keyword_list = keyword[0].split(",")

    return start_date, end_date, keyword_list

if __name__ == '__main__':
    start_date, end_date, keyword_list = get_arguments()

    main(start_date, end_date, keyword_list)
