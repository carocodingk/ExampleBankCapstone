# Data Engineering Capstone Project
## BANK SYSTEM SIMULATION

### Description
This project emulates some of the processes that would take place in a bank. We need to manage an ETL (extraction, transformation, loading) process, a front-end to for the user to interact and input instructions to the system and a data analysis/visualization component to retrieve the data that we need.

At first, we have three JSON files that contain personal information of customers, information about the bank branches, information about transactions during 2018, respectively. The first step is extract this data from the files, transform them into a required format and load them into a database resulting in one table per file. At the same time, we have a fourth source of data from a data API endpoint that we need to include in our database. 