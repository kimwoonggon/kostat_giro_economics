import sys
import json
import urllib.request
import re
from typing import *
import datetime
import pandas as pd
from gunseol_settings import BASE_SETTINGS

Settings = BASE_SETTINGS()

def get_naver_connection(url: str, header_id: str, header_secret: str):
    req = urllib.request.Request(url)
    req.add_header('X-Naver-Client-Id', header_id)
    req.add_header('X-Naver-Client-Secret', header_secret)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as e:
        
        return None

def get_naver_json(kind: str, search_text: str, page_start: str, display_num: str, header_id: str, header_secret: str):
    base = 'https://openapi.naver.com/v1/search'
    node = f'/{kind}.json'
    parameters = f"?query={urllib.parse.quote(search_text)}&start={page_start}&display={display_num}"
    url = base + node + parameters
    raw_json = get_naver_connection(url, header_id, header_secret)
    
    if raw_json == None:
        return None
    else:
        return json.loads(raw_json)

def process_data(post: dict, jsonResult: list):
    
    pDate = datetime.datetime.strptime(post['pubDate'], "%a, %d %b %Y %H:%M:%S +0900")
    if (datetime.datetime.now() - pDate).total_seconds() > int(86400 * Settings.DAYS):
        return jsonResult
    else:
        pDate = pDate.strftime("%Y-%m-%d %H:%M:%S")
        title = post['title']
    del_letters1 = re.compile('[<b>|</b>|&quot]')
    title = del_letters1.sub("", title)
    description = post['description']
    description = del_letters1.sub("", description)
    
    link = post['originallink']
    description, title = filter_article(description=description, title=title)
    if description and title:
        jsonResult.append({"제목":title, "기사요약":description, "링크":link, "날짜":pDate})
    return jsonResult

def filter_article(description: str, title: str):
    for filter in Settings.FILTERS:
        if filter in description or filter in title:
            return None, None
    return description, title

def crawl_data(user_search_list: list, user_name_list: list) -> pd.core.frame.DataFrame:
    
    total_data = pd.DataFrame(columns = ['담당자', '기업체명', '날짜', '제목', '기사요약', '링크'])
    
    for search, user_name in zip(user_search_list, user_name_list):
        print(f"{user_name}님의 {search} 자료를 수집합니다.")
        jsonResult = []
        pre_search_text = Settings.PRE_SEARCH_TEXT
        real_search_text = search
        search_text = real_search_text + ' ' + pre_search_text.replace("(주)", "")
        jsonSearch = get_naver_json(kind = Settings.KIND,
                                    search_text = search_text,
                                    page_start = '1',
                                    display_num = Settings.DISPLAY_NUM,
                                    header_id = Settings.HEADER_ID,
                                    header_secret = Settings.HEADER_SECRET)

        while ((jsonSearch != None) and (jsonSearch['display'] != 0)):
            for post in jsonSearch['items']:
                jsonResult = process_data(post, jsonResult)

            nStart = str(jsonSearch['start'] + jsonSearch['display'])
            

            jsonSearch = get_naver_json(kind = Settings.KIND,
                                        search_text = search_text,
                                        page_start = nStart,
                                        display_num = Settings.DISPLAY_NUM,
                                        header_id = Settings.HEADER_ID,
                                        header_secret = Settings.HEADER_SECRET)

        temp_data = pd.DataFrame(jsonResult, columns = ['날짜', '제목', '기사요약', '링크'])
        temp_data['담당자'] = user_name
        temp_data['기업체명'] = real_search_text
        temp_data = temp_data[['담당자', '기업체명', '날짜', '제목', '기사요약', '링크']]
        total_data = pd.concat([total_data, temp_data], axis=0)

    total_data = total_data.sort_values(by='담당자').reset_index(drop=True)    
    nowtime = datetime.datetime.now()
    nowtime = nowtime.strftime("(%y년%m월%d일%H시%M분%S초)")
    total_data.to_excel(nowtime + Settings.SAVE_FILE, index=False)
    return total_data


if __name__ == "__main__":
    businessname = ['포스코건설']
    personname = ['김웅곤']
    crawl_data(businessname, personname)