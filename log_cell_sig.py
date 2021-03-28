import requests
import datetime
import pandas as pd
import time

def get_sig():
    cur_time = datetime.datetime.now()
    headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://192.168.12.1/web_whw/',
    'Accept-Language': 'en-US,en;q=0.9',
    }

    r = requests.get('http://192.168.12.1/fastmile_radio_status_web_app.cgi', headers=headers, verify=False)

    txt = r.text
    start = txt.find("cell_5G_stats_cfg")
    end = txt.find("cell_LTE_stats_cfg")
    text_5g = txt[start:end]
    text_5g = text_5g.replace("\n","")
    text_5g = text_5g.replace("\n","")
    text_5g = text_5g.replace('cell_5G_stats_cfg":[{"stat":{',"")
    text_5g = text_5g.replace('}}],"',"")
    text_5g = text_5g.replace('"',"")
    d_5g = {}
    for cat in text_5g.split(","):
        l = cat.split(":")
        try:
            d_5g[l[0]]=int(l[1])
        except ValueError:
            d_5g[l[0]]=l[1]
    text_4g = txt[end:]
    text_4g = text_4g.replace("\n","")
    text_4g = text_4g.replace("\n","")
    text_4g = text_4g.replace('cell_LTE_stats_cfg":[{"stat":{',"")
    text_4g = text_4g.replace('}}]}',"")
    text_4g = text_4g.replace('"',"")
    d_4g = {}

    for cat in text_4g.split(","):
        l = cat.split(":")
        try:
            d_4g[l[0]]=int(l[1])
        except ValueError:
            d_4g[l[0]]=l[1]
    d_4g["Time"] = cur_time
    d_5g["Time"] = cur_time
    
    return [d_4g,d_5g]
    

df_5g = pd.read_csv("5g_log.csv", delimiter = ",")
df_4g = pd.read_csv("4g_log.csv", delimiter = ",")

while True:
    new_4g_df = pd.DataFrame(get_sig()[0], index = [0])
    #new_4g_df.insert(loc = 0, column = "time", value = cur_time)
    df_4g = df_4g.append(new_4g_df, ignore_index = True)
    #print(new_4g_df)
    df_4g.to_csv("4g_log.csv",index = False)
    
    new_5g_df = pd.DataFrame(get_sig()[1], index = [0])
    #new_5g_df.insert(loc = 0, column = "time", value = cur_time)
    df_5g = df_5g.append(new_5g_df, ignore_index = True)
    #print(new_5g_df)
    df_5g.to_csv("5g_log.csv",index = False)
    
    time.sleep(1)
