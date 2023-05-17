# -*- coding: utf-8 -*-
# @Time    : 2023/5/16 15:49
# @Author  : lsyhahaha

'''
基于内容的推荐算法根据音乐的特征和用户的偏好，推荐与用户兴趣相似的音乐。
你可以使用Spark提供的机器学习库，如MLlib，来构建和训练基于内容的推荐模型。
'''
import os
os.environ['JAVA_HOME']='/export/server/jdk1.8.0_241'
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.recommendation import ALS
from pyspark.sql import SparkSession

from pyspark.sql import SparkSession
from pyspark.ml.feature import HashingTF, IDF
from pyspark.ml.linalg import Vectors
from pyspark.ml.recommendation import ALS

# 创建SparkSession
spark = SparkSession.builder.appName("Content-Based Recommendation").getOrCreate()

# 加载音乐特征数据
music_features_df = spark.read.csv("../faker_data/music_features.csv", header=True, inferSchema=True)

# 特征提取和转换
hashingTF = HashingTF(inputCol="feature_text", outputCol="rawFeatures", numFeatures=10)
featurizedData = hashingTF.transform(music_features_df)

idf = IDF(inputCol="rawFeatures", outputCol="features")
idfModel = idf.fit(featurizedData)
transformedData = idfModel.transform(featurizedData)

# 构建推荐模型
als = ALS(userCol="user_id", itemCol="music_id", ratingCol="rating", coldStartStrategy="drop")
model = als.fit(transformedData)

# 示例：为用户1推荐5首音乐
# user_id = 1
# user_data = spark.createDataFrame([(user_id,)], ["user_id"])
# user_recommendations = model.recommendForUserSubset(user_data, 5)
#
# # 打印推荐结果
# print(f"Recommendations for User {user_id}:")
# user_recommendations.show(truncate=False)


# 对所有用户进行音乐推荐
all_user_recs = model.recommendForAllUsers(5)
all_user_recs.show()