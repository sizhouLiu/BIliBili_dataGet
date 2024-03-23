from matplotlib import pyplot as plt
import numpy as np
import datetime
import time
import pandas as pd


def draw_heatmap(commit_data,username):
    dates = commit_data.index

    # 创建矩阵
    heatmap = np.zeros((24, 30))
    for i, date in enumerate(dates):

        ts = date.timestamp()
        nowtime = int(time.time())
        day = 29-int((nowtime-int(ts))//60//60/24)
        hour = ((nowtime - int(ts)) // 60 // 60) % 24
        heatmap[hour, day] = commit_data[date]

    # 绘制热力图
    # plt.figure(figsize=(40,40),dpi=50)
    plt.imshow(heatmap, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.title(f"{username} Bilibiliview_at Heatmap")
    plt.yticks(range(24))
    plt.xticks(range(0,30,2))
    plt.xlabel("Day")
    plt.ylabel("hour")
    plt.show()

if "__name__" == "__main__":

    df = pd.read_csv("Stupid__Cat的历史记录.csv", index_col='view_at')
    df.index = pd.DatetimeIndex(df.index)
    draw_heatmap(df.resample("H").count()["title"],username="Stupid_Cat")
