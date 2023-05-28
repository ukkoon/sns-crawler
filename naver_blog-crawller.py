import csv
import json
from bs4 import BeautifulSoup
import requests
# from selenium import webdriver

# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# driver = webdriver.Chrome('chromedriver',options=options)
# driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# driver.implicitly_wait(3)

headers = {
    'authority': 'm.blog.naver.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://m.blog.naver.com/PostList.naver?blogId=vip121265',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
}

# 맛집 블로그 "비밀이야"
blog_id = "jh061158"

def get_posts(blog_id):    
    posts_per_page = 24
    current_page = 1 
    post_ids = []
    
    while True:
        blog_api_url = f"https://m.blog.naver.com/api/blogs/{blog_id}/post-list?categoryNo=0&itemCount={posts_per_page}&page={current_page}&userId="
        response = requests.get(blog_api_url, headers=headers)        
        
        json_object = json.loads(response.text)
        json_response = json_object['result']
        
        posts = json_response['items']
        posts_count = len(json_response['items'])

        # postId = item['logNo']
        # postTitle = item['titleWithInspectMessage']
        # sympathyCnt = item['sympathyCnt']
        # categoryName = item['categoryName']
        # summary = item['briefContents']
        post_ids.extend(list(map(lambda x:{'id':x['logNo'], 'title':x['titleWithInspectMessage']},posts)))        
        
        current_page+=1        
        if posts_count < posts_per_page or current_page>10:
            break        

    return post_ids
        

    
posts = get_posts(blog_id)
result = [['id','title','body']]

for post in posts:
    id = post['id']
    response = requests.get(f"https://m.blog.naver.com/{blog_id}/{id}",headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.text

    id = post['id']
    title = post['title']
    
    body = "".join(line.strip() for line in text.split("\n"))
    body_start_idx = body.find("신고하기")+4
    body_end_idx = body.find("글이전")
    body = body[body_start_idx:body_end_idx]

    result.append([id,title,body])
    
with open(f'naver-blog-{blog_id}.csv', 'w', newline='\n') as f:
    write = csv.writer(f)            
    write.writerows(result)