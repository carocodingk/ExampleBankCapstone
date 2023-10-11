# import pyspark
# import data_transf

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, when, lower, concat_ws, col
from data_transf import phone_format, title_format, time_format

spark = SparkSession.builder.master("local[*]").appName("banksystemSpark").getOrCreate()

''' LOAN CREDIT CARD DATABASE(SQL)
    DATA EXTRACTION phase'''
branchDF = spark.read.json("Credit_Card_Dataset/cdw_sapp_branch.json")
creditDF = spark.read.json("Credit_Card_Dataset/cdw_sapp_credit.json")
customerDF = spark.read.json("Credit_Card_Dataset/cdw_sapp_custmer.json") 

'''Converts python functions into PySpark User Defined Functions'''
phone_format_udf = udf(lambda x: phone_format(x))
title_format_udf = udf(lambda x: time_format(x))
time_format_udf = udf(lambda x: time_format(x))

''' DATA TRANSFORMATION phase'''
branchDF_transformed = branchDF.select( 'BRANCH_CODE', \
                                        'BRANCH_NAME', \
                                        'BRANCH_STREET', \
                                        'BRANCH_CITY', \
                                        'BRANCH_STATE', \
                                        when(branchDF['BRANCH_ZIP'].isNull(), 99999).otherwise(branchDF['BRANCH_ZIP']).alias('BRANCH_ZIP'), \
                                        phone_format_udf('BRANCH_PHONE').alias('BRANCH_PHONE'), \
                                        'LAST_UPDATED')

# branchDF_transformed.show()
# branchDF.printSchema()
# branchDF_transformed.printSchema()

customerDF_transformed = customerDF.select( col('SSN'), \
                                            time_format_udf('FIRST_NAME').alias('FIRST_NAME'), \
                                            lower('MIDDLE_NAME').alias('MIDDLE_MAME'), \
                                            title_format_udf('LAST_NAME').alias('LAST_NAME'), \
                                            'CREDIT_CARD_NO', \
                                            concat_ws(', ', 'STREET_NAME', 'APT_NO').alias('FULL_STREET_ADDRESS'), \
                                            'CUST_CITY', \
                                            'CUST_STATE', \
                                            'CUST_COUNTRY', \
                                            'CUST_ZIP', \
                                            phone_format_udf('CUST_PHONE').alias('CUST_PHONE'), \
                                            'CUST_EMAIL', \
                                            'LAST_UPDATED')
# customerDF_transformed.show()
# customerDF_transformed.printSchema()

creditDF_transformed = creditDF.select( 'CREDIT_CARD_NO', \
                                        'CUST_SSN', \
                                        concat_ws('', 'YEAR',  time_format_udf('MONTH'), time_format_udf('DAY')).alias('TIMEID'), \
                                        'BRANCH_CODE', \
                                        'TRANSACTION_TYPE', \
                                        'TRANSACTION_VALUE', \
                                        'TRANSACTION_ID')
# creditDF_transformed.show()
# creditDF_transformed.printSchema()