import requests
import time
import uuid
import json
import csv
import datetime

host = "https://apis.naver.com/"
path = "cafe-web/cafe2/ArticleListV2.json"

#유럽여행 정보 카페 "유랑"
club_id = "10209062"

menu_id = None
search_per_page = 50
goal_count = 100
iter_num = round(goal_count/search_per_page)
page_last_article_id = None


fields = ['날짜','글쓴이','제목']
rows= []
for page_num in range(1,iter_num+1):    
    args = f"search.club_id={club_id}&search.queryType=lastArticle&search.page={page_num}&search.perPage={search_per_page}"
    if menu_id:
        args+= f"&search.menu_id={menu_id}"

    print(args)

    uri = f"{host}{path}?{args}"    

    if page_last_article_id is not None:
        additonal_args = f"ad=true&uuid={uuid.uuid4()}&adUnit=MW_CAFE_ARTICLE_LIST_RS&search.page_last_article_id={page_last_article_id}&search.replylistorder=&search.firstArticleInReply=false&lastItemIndex=51&lastAdIndex=34"
        uri += f'&{additonal_args}'

    response = requests.get(uri)    
    json_object = json.loads(response.text)
    articles = json_object['message']['result']['articleList']    
         
    if 'item' in articles[0]:
        articles = list(map(lambda x:x['item'],articles))

    for i in range(len(articles)-1,0,-1):
        if 'articleId' in articles[i] :
            page_last_article_id = articles[i]['articleId']
            break
    
    for a in articles:
        write_date_timestamp = datetime.datetime.fromtimestamp(a['write_date_timestamp']/1000) if 'write_date_timestamp' in a else '날짜 없음'
        writer_nickname = a['writer_nickname'] if 'writer_nickname' in a else '닉네임 없음'
        subject = a['subject'] if 'subject' in a else '제목 없음'
        row = [write_date_timestamp,writer_nickname,subject] 
        rows.append(row)

    print(f'success crawling for {page_num}')
    time.sleep(1)    

with open(f'naver-cafe-{club_id}.csv', 'w', newline='\n') as f:
    write = csv.writer(f)        
    write.writerow(fields)
    write.writerows(rows)
    
