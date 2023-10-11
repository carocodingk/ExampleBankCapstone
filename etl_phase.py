# import pyspark
# import data_transf

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from data_transf import phone_format, title_format, time_format

spark = SparkSession.builder.master("local[*]").appName("banksystemSpark").getOrCreate()

''' LOAN CREDIT CARD DATABASE(SQL)
    DATA EXTRACTION phase'''
branchDF = spark.read.json("Credit_Card_Dataset/cdw_sapp_branch.json")
creditDF = spark.read.json("Credit_Card_Dataset/cdw_sapp_credit.json")
customerDF = spark.read.json("Credit_Card_Dataset/cdw_sapp_custmer.json") 

phone_format_udf = udf(lambda x: phone_format(x))
title_format_udf = udf(lambda x: time_format(x))
time_format_udf = udf(lambda x: time_format(x))