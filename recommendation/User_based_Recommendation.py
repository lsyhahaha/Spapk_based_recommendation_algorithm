# -*- coding: utf-8 -*-
# @Time    : 2023/5/16 15:49
# @Author  : lsyhahaha

import os
os.environ['JAVA_HOME']='/export/server/jdk1.8.0_241'
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# 创建 SparkSession
spark = SparkSession.builder \
    .appName("Music Recommendation") \
    .getOrCreate()

# 读取音乐评分数据
data = spark.read.csv("../faker_data/music_ratings.csv", header=True, inferSchema=True)

# 划分数据集为训练集和测试集
(trainingData, testData) = data.randomSplit([0.8, 0.2])

# 构建 ALS 模型
als = ALS(maxIter=10, regParam=0.01, userCol="user_id", itemCol="music_id", ratingCol="rating", coldStartStrategy="drop")
model = als.fit(trainingData)

# 对测试集进行预测
predictions = model.transform(testData)

# 评估模型
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
print("Root Mean Squared Error (RMSE) = " + str(rmse))

# 为用户生成音乐推荐
userRecs = model.recommendForAllUsers(10)  # 为每个用户生成10个推荐
userRecs.show()

# 停止 SparkSession
spark.stop()
