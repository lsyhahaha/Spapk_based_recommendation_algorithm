# -*- coding: utf-8 -*-
# @Time    : 2023/5/16 15:49
# @Author  : lsyhahaha

'''
协同过滤是一种常用的推荐算法，通过分析用户的历史行为和其他用户的行为模式，来预测用户可能感兴趣的音乐。
在Spark中，你可以使用基于矩阵分解的协同过滤算法，如交替最小二乘法（Alternating Least Squares，ALS）。
'''

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import SparkSession
import os

os.environ['JAVA_HOME']='/export/server/jdk1.8.0_241'

# 创建Spark会话
spark = SparkSession.builder.getOrCreate()

# 加载音乐推荐数据（用户ID、音乐ID、评分）
data = spark.read.csv("../faker_data/music_ratings.csv", header=True, inferSchema=True)

# 将数据拆分为训练集和测试集
train_data, test_data = data.randomSplit([0.8, 0.2])

# 创建ALS模型
als = ALS(userCol="user_id", itemCol="music_id", ratingCol="rating", coldStartStrategy="drop")

# 在训练集上拟合ALS模型
model = als.fit(train_data)

# 在测试集上进行预测
predictions = model.transform(test_data)

# 评估预测结果
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
print("Root Mean Squared Error (RMSE)(模型的均方根误差) = " + str(rmse))

# 针对某个用户进行音乐推荐
user_id = 1
user_recs = model.recommendForUserSubset(spark.createDataFrame([(user_id,)]).toDF("user_id"), 5)
user_recs.show()
