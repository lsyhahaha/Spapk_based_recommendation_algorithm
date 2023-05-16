# -*- coding: utf-8 -*-
# @Time    : 2023/5/16 16:12
# @Author  : lsyhahaha

import csv
import random


def music_ratings(k=100):
    print("k = ", k)
    ratings = []
    music_ids = range(1001, 1101+k)  # 音乐ID范围：1001-1100
    user_ids = range(1, 50)  # 用户ID范围：1-20

    for _ in range(k):
        user_id = random.choice(user_ids)
        music_id = random.choice(music_ids)
        rating = round(random.uniform(1.0, 5.0), 1)

        ratings.append({"user_id": user_id, "music_id": music_id, "rating": rating})

    # 保存数据到CSV文件
    with open('../faker_data/music_ratings.csv', 'w', newline='') as csvfile:
        fieldnames = ['user_id', 'music_id', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(ratings)
    print("音乐推荐数据已保存到 music_ratings.csv 文件。")
music_ratings(k=1000)
