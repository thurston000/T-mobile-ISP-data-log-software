import speedtest
import requests
import datetime
import time
import pandas as pd
st = speedtest.Speedtest()
df = pd.read_csv("speed_log.csv", delimiter = ",")
while True:
    speed = st.download()/1000000 #in megabits
    print("speed",speed,"mb")
    cur_time = datetime.datetime.now()
    new_df = pd.Series({"time":cur_time, "speed":speed})
    df = df.append(new_df, ignore_index = True)
    print(new_df)
    df.to_csv("speed_log.csv",index = False)
    time.sleep(900)

