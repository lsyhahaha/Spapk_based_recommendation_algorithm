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
# music_ratings(k=1000)

def music_features(k=1000):
    # 生成k条音乐特征数据
    data = []
    for music_id in range(1, k + 1):
        # 生成随机的特征向量
        feature_vector = [random.random() for _ in range(10)]
        data.append([music_id] + feature_vector)

    # 将数据写入CSV文件
    with open('music_features.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['music_id'] + [f'feature_{i}' for i in range(10)])  # 写入表头
        writer.writerows(data)  # 写入数据

    print(f"{k}条音乐特征数据已生成并写入music_features.csv文件。")


# 调用函数生成1000条音乐特征数据
music_features(1000)
