import mysql.connector
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, when, lower, concat_ws, col, to_timestamp
from data_transf import phone_format, title_format, time_format
from mysql.connector import Error
from secret import db_username, db_password

#####################################################################################################
''' LOAN CREDIT CARD DATABASE(SQL)'''
'''DATA EXTRACTION phase'''
#####################################################################################################
spark = SparkSession.builder.master("local[*]").appName("banksystemSpark").getOrCreate()

branchDF = spark.read.json("Credit_Card_Dataset/cdw_sapp_branch.json")
creditDF = spark.read.json("Credit_Card_Dataset/cdw_sapp_credit.json")
customerDF = spark.read.json("Credit_Card_Dataset/cdw_sapp_custmer.json") 
print(">>>>> Success! Data extracted")

'''Converts python functions into PySpark User Defined Functions'''
phone_format_udf = udf(lambda x: phone_format(x))
title_format_udf = udf(lambda x: title_format(x))
time_format_udf = udf(lambda x: time_format(x))

#####################################################################################################
''' DATA TRANSFORMATION phase'''
#####################################################################################################
branchDF_transformed = branchDF.select( col('BRANCH_CODE').cast('int'), \
                                        'BRANCH_NAME', \
                                        'BRANCH_STREET', \
                                        'BRANCH_CITY', \
                                        'BRANCH_STATE', \
                                        when(branchDF['BRANCH_ZIP'].isNull(), 99999).otherwise(branchDF['BRANCH_ZIP']).cast('int').alias('BRANCH_ZIP'), \
                                        phone_format_udf('BRANCH_PHONE').alias('BRANCH_PHONE'), \
                                        to_timestamp('LAST_UPDATED').alias('LAST_UPDATED'))

# branchDF_transformed.show()
# branchDF.printSchema()
# branchDF_transformed.printSchema()

customerDF_transformed = customerDF.select( col('SSN').cast('int'), \
                                            title_format_udf('FIRST_NAME').alias('FIRST_NAME'), \
                                            lower('MIDDLE_NAME').alias('MIDDLE_NAME'), \
                                            title_format_udf('LAST_NAME').alias('LAST_NAME'), \
                                            'CREDIT_CARD_NO', \
                                            concat_ws(', ', 'STREET_NAME', 'APT_NO').alias('FULL_STREET_ADDRESS'), \
                                            'CUST_CITY', \
                                            'CUST_STATE', \
                                            'CUST_COUNTRY', \
                                            col('CUST_ZIP').cast('int'), \
                                            phone_format_udf('CUST_PHONE').alias('CUST_PHONE'), \
                                            'CUST_EMAIL', \
                                            to_timestamp('LAST_UPDATED').alias('LAST_UPDATED'))
# customerDF_transformed.show()
# customerDF_transformed.printSchema()

creditDF_transformed = creditDF.select( 'CREDIT_CARD_NO', \
                                        concat_ws('', 'YEAR',  time_format_udf('MONTH'), time_format_udf('DAY')).alias('TIMEID'), \
                                        col('CUST_SSN').cast('int'), \
                                        col('BRANCH_CODE').cast('int'), \
                                        'TRANSACTION_TYPE', \
                                        'TRANSACTION_VALUE', \
                                        col('TRANSACTION_ID').cast('int'))
# creditDF_transformed.show()
# creditDF_transformed.printSchema()
# creditDF.printSchema()
print(">>>>> Success! Data transformed")

#####################################################################################################
''' DATA LOADING PHASE'''
#####################################################################################################
try:
    #Establish a connection to MySQL Workbench to create database
    db_connection = mysql.connector.connect(user=db_username, password=db_password)
    db_cursor = db_connection.cursor()
    db_cursor.execute("CREATE DATABASE IF NOT EXISTS creditcard_capstone;") #avoids error if the db already exists
    print('>>>>> Success! Connection to database successful. Database created')
except Error as e:
    print('>>>>> Failed! Unable to connect to Example bank database: {}'.format(e))
finally:
    if db_connection and db_connection.is_connected():
        db_cursor.close()
        db_connection.close()
        print('>>>>> Success! Connection to database has been closed')


branchDF_transformed.write.format("jdbc").mode("overwrite") \
  .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
  .option("dbtable", "creditcard_capstone.CDW_SAPP_BRANCH") \
  .option("user", db_username) \
  .option("password", db_password) \
  .save()

customerDF_transformed.write.format("jdbc").mode("overwrite") \
  .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
  .option("dbtable", "creditcard_capstone.CDW_SAPP_CUSTOMER") \
  .option("user", db_username) \
  .option("password", db_password) \
  .save()

creditDF_transformed.write.format("jdbc").mode("overwrite") \
  .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
  .option("dbtable", "creditcard_capstone.CDW_SAPP_CREDIT_CARD") \
  .option("user", db_username) \
  .option("password", db_password) \
  .save()

print(">>>>> Success! Data loaded into database")

#####################################################################################################
''' LOAN APPLICATION DATASET - ACCESS TO LOAN API ENDPOINT
    LOADING PHASE'''
#####################################################################################################
loan_url = 'https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json'
response = requests.get(loan_url) #fetch data from API
if response.status_code == 200:
    loan = response.json()
    loanDF = spark.createDataFrame(loan)
    loanDF.write.format("jdbc").mode("overwrite") \
        .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
        .option("dbtable", "creditcard_capstone.CDW_SAPP_LOAN_APPLICATION") \
        .option("user", db_username) \
        .option("password", db_password) \
        .save()
    print('>>>>> Success! Loan Data loaded into database. Status code: {}'.format(response.status_code))
else:
    print('>>>>> Failed! Unable to load data into database. Status code: {}'.format(response.status_code))