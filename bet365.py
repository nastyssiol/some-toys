import requests
import fake_useragent
import re
import csv
from datetime import datetime, timedelta

def get_time_difference(the_data):
    now = datetime.now()
    formatted_time = str(now.strftime('%Y-%m-%dT%H:%M:%SZ'))
    the_data = the_data[:20]
    datetime_obj = datetime.fromisoformat(the_data[:-1])  # Преобразуем строку в объект datetime
    updated_datetime_obj = datetime_obj + timedelta(hours=3)  # Добавляем три часа
    updated_the_data = updated_datetime_obj.isoformat() + "Z"
    
    if updated_datetime_obj.month > datetime_obj.month:
        updated_datetime_obj = updated_datetime_obj.replace(month=datetime_obj.month)
    
    the_difference = (updated_datetime_obj - now).total_seconds() // 3600
    return int(the_difference)

user = fake_useragent.UserAgent().random
url='https://nlsportv2.anyplay.pro/sport'
headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'https://bet-365.store',
    'Referer': 'https://bet-365.store/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.739 Yowser/2.5 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = '{"devmode":false,"project":"78098","lang":"ru","type":"line","sport":"201"}'

session = requests.Session()
response = session.post(url=url, headers=headers, data=data)
results = response.json().get('data')[0].get('leagues')

main_url = 'https://bet-365.store/line/201/'
output = dict()
output['https://bet-365.store/line/201/'] = list()
for result in results:
    events = result.get('events')
    league_id = str(result.get('league_id'))
    # print(output)
    for event in events:
        time = event.get('start_stamp')
        print(time)
        time_diffetence = get_time_difference(time)
        print(time_diffetence)
        if time_diffetence<=48 and time_diffetence>=2:
            id = str(event.get('id'))
            match_url = main_url +league_id+'/'+id
            pre_output = dict()
            pre_output[match_url] = list()
            odds = event.get('odds')
            od_output = {
            
            }
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'ru,en;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'text/plain;charset=UTF-8',
                'Origin': 'https://bet-365.store',
                'Referer': 'https://bet-365.store/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.739 Yowser/2.5 Safari/537.36',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            devmode = 'false'
            project = "78098"
            lang = "ru"
            type = "line"
            event = id
            sport = "201"
            league = league_id
            period = 0
            data = '{"devmode":false,"project":"78098","lang":"ru","type":"line","event":"6332669","sport":"201","league":"8673","period":0}'
            json_string = '{"devmode":' + devmode + ',"project":"' + project + '","lang":"' + lang + '","type":"' + type + '","event":"' + event + '","sport":"' + sport + '","league":"' + league + '","period":' + str(period) + '}'
            data = json_string
            
            response = session.post('https://nlsportv2.anyplay.pro/event', headers=headers, data=data).json()
            # print(response)
            # response = session.post('https://1win.direct/microservice/ask', headers=headers, json=json_data).json()
            data = response.get('data')
            odds = data.get('odds')
            for d, odd in enumerate(odds[:4]):
                naming = odd.get('col_n')
                ods = odd.get('od')
                od_output[f'name{d+1}'] = odd.get('col_n')
                for i, od in enumerate(ods):
                        if od.get('n') == 'Победитель' or od.get('n') == 'Ничья':
                            continue
                        od_output[od.get('n')] = od.get('c')
            pre_output[match_url].append(od_output)
            output['https://bet-365.store/line/201/'].append(pre_output)
            # print(match_url)
            # print(id)
            # print(time_diffetence)
print(output)


