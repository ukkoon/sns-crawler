import json
import time
import requests

cookies = {
    'ig_did': 'AD27248C-0EB3-4ECB-84B2-BB9843CEE612',
    'ig_nrcb': '1',
    'dpr': '2',
    'csrftoken': 'p5pNimeaMCrHd96gFZiW6ys0xChKqGfw',
    'mid': 'ZAW6dgAEAAF-aq8zw5Q6IXlgSlka',
    'datr': 'G7sFZLI94xST_3d-x2VjhZbS',
}

headers = {
    'authority': 'www.instagram.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    # 'cookie': 'ig_did=AD27248C-0EB3-4ECB-84B2-BB9843CEE612; ig_nrcb=1; dpr=2; csrftoken=p5pNimeaMCrHd96gFZiW6ys0xChKqGfw; mid=ZAW6dgAEAAF-aq8zw5Q6IXlgSlka; datr=G7sFZLI94xST_3d-x2VjhZbS',
    'referer': 'https://www.instagram.com/p/CoeS8sapt8K/',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
    'viewport-width': '1508',
    'x-asbd-id': '198387',
    'x-csrftoken': 'p5pNimeaMCrHd96gFZiW6ys0xChKqGfw',
    'x-ig-app-id': '1217981644879628',
    'x-ig-www-claim': '0',
    'x-requested-with': 'XMLHttpRequest',
}

results = []
user_id = 173560420
# response = requests.get(f'', headers=headers,cookies=cookies )
# json_object = json.loads(response.text)
# items = json_object['items']
max_id = None

for i in range(10):
    url = f"https://www.instagram.com/api/v1/feed/user/{user_id}/?count=5"
    if max_id:
        url += f"&max_id={max_id}"

    try:
        response = requests.get(url, headers=headers,cookies=cookies )
        print(response.status_code)
        json_object = json.loads(response.text)
        items = json_object['items']
        max_id = items[-1]['id']

        caption_texts = list(map(lambda x:x['caption']['text'], items))
        results.extend(caption_texts)
        print(len(items))
        print(caption_texts)
        time.sleep(1)
    except Exception as e:
        print(e)
        break

print(results)
#item : taken_at, pk, id, device_timestamp, media_type