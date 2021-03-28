import speedtest
import requests
import datetime
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
st = speedtest.Speedtest()
df = pd.read_csv("speed_log.csv", delimiter = ",")
while True:
    for i in range(30):
        speed = st.download()/1000000 #in megabits
        print("speed",speed,"mb")
        x = datetime.datetime.now().strftime("%S")
        y = speed
        plt.scatter(x, y)
        plt.title("Real Time plot")
        plt.xlabel("Time")
        plt.ylabel("Download Speed")
        plt.pause(.00000000000000000000000000000000000000000001)
    plt.clf()


