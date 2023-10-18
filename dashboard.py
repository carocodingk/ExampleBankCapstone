import mysql.connector
import re
import matplotlib.pyplot as plt
# import datetime

from mysql.connector import Error
from text_variables import welcome, continue_text, main_menu_text, trans_menu_text, trans_menu_text1, trans_menu_text2, trans_type_dict, trans_menu_text3, trans_states_dict
from text_variables import cust_menu_text, cust_menu_text1, cust_menu_text2, cust_update_dict
from text_variables import viz_text, viz_text1, viz_text2, viz_months_dict, viz_text3, viz_text4, viz_text5, viz_text6, viz_text7, viz_text8, viz_text9
from data_transf import title_format, print_zip_report, print_short_report, print_monthly_bill, print_transactions, print_customer_details, privacy_string
from secret import db_username, db_password

exit_flag = False

''' This function is a placeholder to generalize functions for 3 or parameters. In only prints invalid option 
    and then the loop continues until a valid option is entered. Menu_option is just a placeholder'''
def invalid_option(menu_option):
    print('Invalid option. Try again')

def menu_box(menu_msg, method1, method2, method3, method4):
    while(not exit_flag):         
        print(menu_msg)
        menu_option = input()
        if menu_option == '1':
            method1(menu_option)
        elif menu_option == '2':
            method2(menu_option)
        elif menu_option == '3':
            method3(menu_option)
        elif menu_option == '4':
            method4(menu_option)
        elif menu_option == '9':
            print('>>>>> Back to previous menu')
            break
        elif menu_option == '0':
            exit_program()
        else:
            print(">>>>> Invalid option. Try again")
                
def exit_program():
    global exit_flag 
    exit_flag = True
    print(">>>>> Exit the program")

def continue_method():
    print(continue_text)
    continue_key = input()
    if continue_key == '9':
        return False
    elif continue_key == '0':
        exit_program()
        return False
    else:
        return True    

def transactions_menu():
    menu_box(trans_menu_text, transactions_zipcode, transactions_type, transactions_state, invalid_option)

def transactions_zipcode(null):
    zipcode = '0000' #initial value to enter in loop
    date = '01/1234'
    continue_inquiry = True

    while (continue_inquiry):
        continue_inquiry = False
        print(trans_menu_text1)
        zipcode = input()
        if (zipcode == '9'):
            break
        print("Enter month and year (mm/yyyy):")
        date = input()
        if (date == '9'):
            break
        elif (zipcode.isnumeric() and len(zipcode) == 5 and re.match("\d\d/\d\d\d\d", date)):
            date1 = date[3:7] + date[0:2]
            query = """SELECT cred.CREDIT_CARD_NO, cred.BRANCH_CODE, cred.TIMEID, cred.TRANSACTION_ID, cred.TRANSACTION_TYPE, cred.TRANSACTION_VALUE
                    FROM cdw_sapp_credit_card AS cred 
                    INNER JOIN cdw_sapp_customer USING(CREDIT_CARD_NO) 
                    WHERE CUST_ZIP = {} AND cred.TIMEID LIKE '{}%'
                    ORDER BY cred.TIMEID DESC""".format(zipcode, date1)
            db_cursor.execute(query)
            all_transactions = db_cursor.fetchall()
            print_zip_report(date, zipcode, all_transactions)
        else:
            print('Your input is invalid. Try again')
        continue_inquiry = continue_method()

def transactions_type(null):
    continue_inquiry = True
    while (continue_inquiry):
        continue_inquiry = False #Prevents that it keeps asking once a result is delivered
        print(trans_menu_text2)
        trans_type = input()
        if (trans_type.isnumeric()):
            if (int(trans_type) in range(1,8)):
                trans_type_name = trans_type_dict[trans_type]
                query = """ SELECT COUNT(TRANSACTION_ID), SUM(TRANSACTION_VALUE)
                FROM CDW_SAPP_CREDIT_CARD
                WHERE TRANSACTION_TYPE = '{}'""".format(trans_type_name)
                db_cursor.execute(query)
                all_transactions = db_cursor.fetchall()
                print_short_report(trans_type_name, all_transactions)
            elif (trans_type == '9'):
                break
            elif (trans_type == '0'):
                exit_program()
                break
            else:
                print('Invalid option. Try again')
        else:
            print('Invalid option. Try again')
        continue_inquiry = continue_method() #if a key is entered, we can keep checking

def transactions_state(menu_option):
    print("here " + menu_option)
    continue_inquiry = True
    while(continue_inquiry):
        continue_inquiry = False
        print(trans_menu_text3)
        state = input().upper()
        if (len(state) > 2 and state in trans_states_dict.keys()):
            state = trans_states_dict[state]
        query = """ SELECT COUNT(TRANSACTION_ID), SUM(TRANSACTION_VALUE)
                    FROM CDW_SAPP_CREDIT_CARD
                    INNER JOIN CDW_SAPP_BRANCH USING (BRANCH_CODE)
                    WHERE BRANCH_STATE = '{}'""".format(state)
        db_cursor.execute(query)
        all_transactions = db_cursor.fetchall()
        print_short_report(state, all_transactions )
        continue_inquiry = continue_method()

def customers_menu():
    menu_box(cust_menu_text, customers_show_details, customers_show_details, customers_show_operations, customers_show_operations)

def customers_search(menu_option, method):
    continue_inquiry = True
    while (continue_inquiry):
        continue_inquiry = False
        print(cust_menu_text1)
        lookup = input()
        if lookup == '1':
            print('Enter SSN:')
            ssn = input()
            method('cust.SSN', ssn, 'x', menu_option)
        elif lookup == '2':
            print('Enter credit card number:')
            cred_card = input()
            method('cust.CREDIT_CARD_NO', cred_card, 'x', menu_option)
        elif lookup == '3':
            print('Enter first name:')
            first_name = title_format(input()) #converts to title case format like in db
            print('Enter last name')
            last_name = title_format(input())
            method('cust.FIRST_NAME', first_name, last_name, menu_option)
        elif lookup == '9':
            break
        elif lookup == '0':
            exit_program()
            break
        else:
            print('Invalid option. Try again')
            continue_inquiry = True


def customers_show_details(menu_option):
    customers_search(menu_option, customers_query_details)

#menu_option just a place_holder    
def customers_query_details(sql_key, value1, value2, menu_option):
    continue_inquiry = True
    while(continue_inquiry):
        query = """ SELECT *
                    FROM cdw_sapp_customer AS cust
                    WHERE {} = '{}'""".format(sql_key, value1)
        if value2 != 'x': #If the search is by first and last name. We need to values
            query = query + " AND cust.LAST_NAME = '{}';".format(value2)
        db_cursor.execute(query)
        all_details = db_cursor.fetchone()
        if all_details is not None:
            credit_card_no = all_details[4]
            print_customer_details(all_details)
        else:
            print('This customer does not exist in the database')
        
        if menu_option == '1':
            print("Press   (9) Return to previous menu \n        (0) Exit program")
            continue_key = input()
            if continue_key == '9':
                continue_inquiry = False
            elif continue_key == '0':
                exit_program()
                break
        else:
            print("Press   Any key to continue \n        (0) Exit program")
            continue_key = input()
            if continue_key == '0':
                exit_program()
                break
            else:
                break
                

    if menu_option == '2' and exit_flag == False: #update customer's details
        customers_update_details(credit_card_no)
        print('AT THIS POINT ' + menu_option)

def customers_update_details(credit_card_no):
    save_updates = False
    updated_data = ""
    while (not save_updates):
        print(cust_menu_text2)
        option = input().upper()
        if option in cust_update_dict.keys():
            field = cust_update_dict[option]
            print("New value for {}".format(field))
            new_value = input()
            if field == 'CUST_ZIP':
                updated_data = updated_data + " {} = {},".format(field, new_value)
                print(type(new_value))
            else:
                updated_data = updated_data + " {} = '{}',".format(field, new_value)
        elif option == '8':
            save_updates = True
            # time_now = datetime.datetime.now()
            # print(time_now)
            time_now = 'CURRENT_TIMESTAMP'
            # updated_data = updated_data[0:len(updated_data)-1]
            updated_data = updated_data + " {} = {}".format('LAST_UPDATED', time_now)
            update = """UPDATE cdw_sapp_customer
                        SET {}
                        WHERE CREDIT_CARD_NO = '{}'""".format(updated_data, credit_card_no)
            # print(update)
            db_cursor.execute(update)
            db_connection.commit()
            print('Data has been updated')
        elif option == '9':
            break
        elif option == '0':
            exit_program()
            break #We don't use save_updates because we are not saving the changes. 
        else:
            print("Invalid option. Try again")


def customers_show_operations(menu_option):
    customers_search(menu_option, customers_query_transactions)


def customers_query_transactions(sql_key, value1, value2, menu_option):
    #Phase 1: retrieves or assigns the credit card number as criteria to search the database
    subquery = ""
    if (sql_key == 'cust.SSN'): #Search by ssn
        subquery = """  SELECT CREDIT_CARD_NO
                        FROM cdw_sapp_customer 
                        WHERE SSN = '{}'""".format(value1)
    elif (sql_key == 'cust.CREDIT_CARD_NO'):
        identifier = value1
        sql_key = 'CREDIT_CARD_NO'
    elif sql_key == 'cust.FIRST_NAME': #Search by first and last name
        subquery = """  SELECT CREDIT_CARD_NO
                        FROM cdw_sapp_customer AS cust
                        WHERE cust.FIRST_NAME = '{}' AND cust.LAST_NAME = '{}'""".format(value1, value2)
        
    if len(subquery) > 0:   #if the search is by credit card, we don't need to retrieve it
        db_cursor.execute(subquery)
        data = db_cursor.fetchone()
        sql_key = 'CREDIT_CARD_NO' #so we can use one query statement for all
        if data is not None:
            identifier = data[0]
        else:
            identifier = ' '

    #Phase 2: General query for transactions details with credit card number as search criteria
    query1 = """ SELECT TIMEID, TRANSACTION_ID, TRANSACTION_TYPE, TRANSACTION_VALUE
                FROM cdw_sapp_credit_card AS cred
                WHERE {} = '{}'""".format(sql_key, identifier)
    
    #Phase 3: Select specific time period. If monthly statement just month/year. If transactions asks for two dates,
    if menu_option == '3': #monthly bill
        print('Enter date (mm/yyyy):')
        date = input()
        date1 = date[3:7]+date[0:2] #Format as db
        query1 = query1 + "AND TIMEID like '{}%'".format(date1) #Queries only for that month
        # Find customer's details for bill as well as number of transactions and total for that month
        query2 = """SELECT  CREDIT_CARD_NO, FIRST_NAME, MIDDLE_NAME, LAST_NAME, FULL_STREET_ADDRESS, CUST_CITY, CUST_STATE, 
                            CUST_COUNTRY, CUST_ZIP, CUST_EMAIL,
                            COUNT(TRANSACTION_ID), SUM(TRANSACTION_VALUE)
                    FROM cdw_sapp_credit_card 
                    INNER JOIN cdw_sapp_customer USING (CREDIT_CARD_NO)
                    WHERE {} = '{}' AND TIMEID like '{}%'
                    GROUP BY CREDIT_CARD_NO, FIRST_NAME, MIDDLE_NAME, LAST_NAME, FULL_STREET_ADDRESS, CUST_CITY, CUST_STATE, CUST_COUNTRY, CUST_ZIP, CUST_EMAIL""".format(sql_key, identifier, date1)
    elif menu_option == '4': #transactions between mm1/yyyy1 and mm2/yyyy2
        print('Enter starting date (mm/yyyy):')
        date1 = input()
        temp1 = date1[3:7]+date1[0:2] #convert to db format
        print('Enter ending date (mm/yyyy):')
        date2 = input()
        temp2 = date2[3:7]+date2[0:2]
        if (int(temp1) > int(temp2)):   #Check if first time input is earlier than the second. Rectify if not
            temp = date1
            date1 = date2
            date2 = temp
        dates = (date1, date2)
        date1 = int(date1[3:7]+date1[0:2]+'01')
        date2 = int(date2[3:7]+date2[0:2]+'31') #it doesn't matter that a month has 28, 29, 30 days. No filtering error possible
        query2 = """SELECT FIRST_NAME, MIDDLE_NAME, LAST_NAME
                    FROM cdw_sapp_customer
                    WHERE CREDIT_CARD_NO = '{}'""".format(identifier)

    # Phase 4: Complete and execute de query for all transactions
    db_cursor.execute(query2)
    account_summary = db_cursor.fetchone()
    query1 = query1 + 'ORDER BY TIMEID DESC'
    db_cursor.execute(query1)
    all_transactions = db_cursor.fetchall()

    # Phase 5: Output the data retrieved in their respective format
    if menu_option == '3':  #Monthly bill
        print_monthly_bill(date, account_summary, all_transactions)
    elif menu_option == '4': #Transactions between dates
        print_transactions(date1, date2, dates, account_summary, identifier, all_transactions)

"""Find and plot which transaction type has the highest transaction count."""
def viz_transactions_types(null):
    query = """  SELECT TRANSACTION_TYPE, COUNT(DISTINCT TRANSACTION_ID) AS COUNT
    FROM cdw_sapp_credit_card
    GROUP BY TRANSACTION_TYPE
    ORDER BY COUNT DESC;"""
    db_cursor.execute(query)
    all_data = db_cursor.fetchall()
    trans_type = []
    trans_count = []
    for t in all_data:
        trans_type.append(t[0])
        trans_count.append(t[1])
    all_data.sort()
    print(viz_text3.format(all_data[0][0].upper(), all_data[0][1]))
    plt.bar(trans_type, trans_count)
    plt.grid(linestyle='--')
    plt.title("Quantity of transactions by type during 2018")
    plt.xlabel('Transaction types')
    plt.ylabel('Quantity of transactions')
    plt.show()

"""Find and plot which state has a high number of customers."""
def viz_high_number_customers(null):
    query = """ SELECT CUST_STATE, COUNT(DISTINCT CREDIT_CARD_NO) AS COUNT
                FROM cdw_sapp_customer
                GROUP BY CUST_STATE
                ORDER BY COUNT DESC
                LIMIT 5;"""
    db_cursor.execute(query)
    all_data = db_cursor.fetchall()
    cust_state = []
    cust_count = []
    for c in all_data:
        cust_state.append(c[0])
        cust_count.append(c[1])
    print(viz_text4.format(cust_state[0], cust_count[0]))
    # print(cust_state)
    # print(cust_count)
    plt.bar(cust_state, cust_count)
    plt.title("Comparisson between the top 5 states with the most customers during 2018")
    plt.xlabel('States')
    plt.ylabel('Number of customers')
    plt.show()


"""Find and plot the sum of all transactions for the top 10 customers, and which customer has the highest transaction amount.
Hint (use CUST_SSN).  Don’t show ppi (ssn) how to represent?"""
def viz_top_customer_transactions(null):
    print("testing")
    query = """ SELECT CUST_SSN, SUM(TRANSACTION_VALUE) AS TOTAL
                FROM cdw_sapp_credit_card
                GROUP BY CUST_SSN
                ORDER BY TOTAL DESC
                LIMIT 10;"""
    db_cursor.execute(query)
    all_data = db_cursor.fetchall()
    cust_id =[]
    cust_total = []
    counter = 1
    for data in all_data:
        cust_id.append('Client '+ str(counter)) #To maintain their anonimaty

        cust_total.append(round(data[1],2))
        counter += 1
    query1 = """SELECT FIRST_NAME, MIDDLE_NAME, LAST_NAME, CUST_CITY, CUST_STATE, cust.CREDIT_CARD_NO
                FROM cdw_sapp_customer AS cust
                INNER JOIN cdw_sapp_credit_card AS cred ON cust.SSN = cred.CUST_SSN
                WHERE SSN = '{}'
                GROUP BY cust.CREDIT_CARD_NO, FIRST_NAME, MIDDLE_NAME, LAST_NAME, CUST_CITY, CUST_STATE;""".format(str(all_data[0][0]))
    db_cursor.execute(query1)
    cust = db_cursor.fetchone()
    print(viz_text5.format(cust[0].upper(), cust[1].upper(), cust[2].upper(), cust[3], cust[4], privacy_string(cust[5]), cust_total[0]))
    plt.bar(cust_id, cust_total)
    plt.title('Comparisson of total transaction value between top 10 customers')
    plt.xlabel('Customers')
    plt.ylabel('Total value of transactions ($)')
    plt.show()


"""Find and plot the percentage of applications approved for self-employed applicants."""
def viz_approved_applications(null):
    criteria = [('Y', 'Yes'), ('N', 'Yes'), ('Y', 'No'), ('N', 'No')]
    applications = [] #[self_employed_approved, self_employed_rejected, not_self_employed_approved, not_self_employed_rejected]
    desc = ['Approved, self-employed', 'Rejected, self-employed', 'Approved, not self-employed', 'Rejected, not self-employed']
    for c in criteria:
        query = """SELECT COUNT(DISTINCT Application_ID)
                    FROM cdw_sapp_loan_application
                    WHERE Application_Status = '{}' AND Self_Employed = '{}';""".format(c[0], c[1])
        db_cursor.execute(query)
        data = db_cursor.fetchone()
        applications.append(data[0])
    total_applications = sum(applications)
    percentage_application = []
    for i in applications:
        percentage_application.append(round(i * 100 / total_applications, 2))
    print(viz_text8.format(percentage_application[0], applications[0], total_applications))
    explode_list = [0.2, 0, 0, 0]
    plt.pie(percentage_application,  autopct='%1.1f%%', explode=explode_list)
    plt.legend(desc, bbox_to_anchor=(1,0.75))
    plt.title('Distribution of loan application results according to employment type')
    plt.show()


"""Find the percentage of rejection for married male applicants."""
def viz_rejected_marital(null):
    #(Approved, Gender, Married)
    criteria = [('Y', "Male", "Yes"), ('Y', "Male", "No"), ('Y', "Female", "Yes"), ('Y', "Female", "No"),
                ('N', "Male", "Yes"), ('N', "Male", "No"), ('N', "Female", "Yes"), ('N', "Female", "No")]
    desc = ['Approved, Male, Married', 'Approved, Male, Not married', 'Approved, Female, Married', 'Approved, Female, Not married',
            'Rejected, Male, Married', 'Rejected, Male, Not married', 'Rejected, Female, Married', 'Rejected, Female, Not married']
    applications = []
    for i in criteria:
        query = """ SELECT COUNT(DISTINCT Application_ID)
                    FROM cdw_sapp_loan_application
                    WHERE Application_Status = '{}' AND Gender = '{}' AND Married = '{}';""".format(i[0], i[1], i[2])
        db_cursor.execute(query)
        data = db_cursor.fetchone()
        applications.append(data[0])
    total_applications = sum(applications)
    percentage_application = []
    for i in applications:
        percentage_application.append(round(i * 100 / total_applications))
    print(viz_text6.format(percentage_application[4], applications[4], total_applications))
    explode_list = [0,0,0,0,0.2,0,0,0]
    plt.subplots(figsize =(10, 7))
    plt.pie(percentage_application, autopct='%1.1f%%', explode=explode_list)
    plt.title('Distribution of loan application results according to gender and marital status')
    plt.legend(desc, bbox_to_anchor=(1,0.75))
    plt.show()

"""Find and plot the top three months with the largest volume of transaction data."""
def viz_top_months(null):
    month_values = []
    for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        query = """ SELECT SUM(TRANSACTION_VALUE)
                    FROM cdw_sapp_credit_card
                    WHERE TIMEID LIKE '____{}__';""".format(month)
        db_cursor.execute(query)
        amount = db_cursor.fetchone()
        month_values.append((month, round(amount[0],2)))
    month_values.sort(key=lambda a:a[1], reverse=True)
    top_months = [month_values[0], month_values[1], month_values[2]]
    months = [viz_months_dict[month_values[0][0]], viz_months_dict[month_values[1][0]], viz_months_dict[month_values[2][0]]]
    amounts = [month_values[0][1], month_values[1][1], month_values[2][1]]
    print(viz_text7.format(months[0], top_months[0][1], months[1], top_months[1][1], months[2], top_months[2][1]))
    #First subplot - plot of total amount
    plt.subplot(1,2,1)
    plt.bar(months, amounts)
    plt.title("Top 3 months with highest transaction value in 2018")
    plt.xlabel('Months')
    plt.ylabel('Transaction value ($)')

    #Second subplot - focused on $200,000 and up to see difference
    plt.subplot(1,2,2)
    plt.bar(months, amounts)
    plt.title("Difference between top 3 months in 2018")
    plt.ylim(200000, 206000)
    plt.xlabel('Months')
    plt.ylabel('Transaction value ($)')
    plt.show()



"""Find and plot which branch processed the highest total dollar value of healthcare transactions."""
def viz_branch_healthcare(null):
    query = """ SELECT BRANCH_CODE, ROUND(SUM(TRANSACTION_VALUE),2) AS TOTAL
                FROM cdw_sapp_credit_card
                WHERE TRANSACTION_TYPE = 'Healthcare'
                GROUP BY BRANCH_CODE
                ORDER BY TOTAL DESC
                LIMIT 8;"""
    db_cursor.execute(query)
    branch_value = db_cursor.fetchall()
    branch_codes, amounts = tuple_extraction(branch_value) #data is organized from greatest amount to least
    branches = []
    counter = 0
    for code in branch_codes:
        if counter == 0:
            query1 = """SELECT branch_code, BRANCH_NAME, BRANCH_STREET, BRANCH_CITY, BRANCH_STATE, BRANCH_ZIP
                        FROM cdw_sapp_branch
                        WHERE BRANCH_CODE = {};""".format(code)   
            db_cursor.execute(query1)
            top_branch_data = db_cursor.fetchone()
            print(viz_text9.format(top_branch_data[1], top_branch_data[0], top_branch_data[2], top_branch_data[3], top_branch_data[4], top_branch_data[5], amounts[0]))
        query1 = """SELECT branch_code, BRANCH_CITY, BRANCH_STATE
                    FROM cdw_sapp_branch
                    WHERE BRANCH_CODE = {};""".format(code)
        db_cursor.execute(query1)
        branch_data = db_cursor.fetchone()
        text = "{}-{}, {}".format(branch_data[0], branch_data[1], branch_data[2])
        branches.append(text)
        counter += 1
    plt.barh(branches, amounts)
    plt.title('Top 8 of branches with highest total value of healthcare transactions', weight='bold')
    plt.ylabel('Branch ID, City, State')
    plt.xticks(rotation = 30)
    plt.xlabel('Total Amount ($)')
    plt.show()

def tuple_extraction(ls):
    first_list = []
    second_list = []
    for item in ls:
        first_list.append(item[0])
        second_list.append(item[1])
    return first_list, second_list

def visualizations():
    continue_inquiry = True
    while (continue_inquiry):
        continue_inquiry = False
        print(viz_text)
        option = input()
        if option == '1':
            menu_box(viz_text1, viz_transactions_types, viz_high_number_customers, viz_top_customer_transactions, invalid_option)
        elif option == '2':
            menu_box(viz_text2, viz_approved_applications, viz_rejected_marital, viz_top_months, viz_branch_healthcare)
            print('here')
        elif option == '9':
            break
        elif option == '0':
            exit_program()
            break
        else:
            print("Invalid option. Try again")
            continue_inquiry = True



try:
    #   Establish connection to local database server
    db_connection = mysql.connector.connect(
        host = 'localhost',
        database = 'creditcard_capstone',
        user = db_username,
        password = db_password
    )
    db_cursor = db_connection.cursor()   
    print('>>>>> Success! Connection to database established')
    while (not exit_flag):
        print(welcome)
        print(main_menu_text)
        main_menu_option = input()
        if main_menu_option == '1':
            transactions_menu()
        elif main_menu_option == '2':
            customers_menu()
        elif main_menu_option == '3':
            visualizations()
        elif main_menu_option == '0':
            exit_flag = True
            print("exit program. loop1")
        else:
            print("Invalid option. Try again")
except Error as e:
    print('>>>>> Failed! Unable to establish connection to database server: {}'.format(e))
finally:
    if db_connection.is_connected():
        db_cursor.close()
        db_connection.close()
        print('>>>>> Success! Connection to database closed')