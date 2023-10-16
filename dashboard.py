import mysql.connector
import re

from mysql.connector import Error
from text_variables import welcome, continue_text, main_menu_text, trans_menu_text, trans_menu_text1, trans_menu_text2, trans_type_dict, trans_menu_text3, trans_states_dict
from text_variables import cust_menu_text, cust_menu_text1
from data_transf import title_format
from secret import db_username, db_password

exit_flag = False

def do_nothing(self):
    pass

''' This function is a placeholder to generalize functions for 3 or parameters. In only prints invalid option 
    and then the loop continues until a valid option is entered'''
def invalid_option():
    print('Invalid option. Try again')

class MenuBox:
    def __init__(self, menu_msg, method1, method2, method3):  #constructor
        self.menu_msg = menu_msg
        self.method1 = method1
        self.method2 = method2
        self.method3 = method3

    def menu_box(self):
        print("good morning")
        while(not exit_flag):         
            print(self.menu_msg)
            menu_option = input()
            print('you chose {}'.format(menu_option))
            if menu_option == '1':
                self.method1(self)
            elif menu_option == '2':
                self.method2(self)
            elif menu_option == '3':
                self.method3(self)
            elif menu_option == '4':
                self.method4(self)
            elif menu_option == '9':
                print('Back to previous menu')
                break
            elif menu_option == '0':
                print("Exit the program")
                self.exit_program()
            else:
                print("Invalid option. Try again")
                
    def exit_program(self):
        global exit_flag 
        exit_flag = True

def continue_method():
    print(continue_text)
    continue_key = input()
    if continue_key == '9':
        return False
    elif continue_key == '0':
        global exit_flag 
        exit_flag = True
        return False
    else:
        return True    

def transactions_menu():
    tr = MenuBox(trans_menu_text, transactions_zipcode, transactions_type, transactions_state, invalid_option)
    tr.menu_box()

def transactions_zipcode(self):
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
            query = """SELECT cred.CREDIT_CARD_NO, cred.TIMEID, cred.BRANCH_CODE, cred.TRANSACTION_TYPE, cred.TRANSACTION_VALUE, cred.TRANSACTION_ID
                    FROM cdw_sapp_credit_card AS cred INNER JOIN cdw_sapp_customer USING(CREDIT_CARD_NO) 
                    WHERE CUST_ZIP = {} AND cred.TIMEID LIKE '{}%'
                    ORDER BY cred.TIMEID DESC""".format(zipcode, date1)
            db_cursor.execute(query)
            all_transactions = db_cursor.fetchall()
            print(type(all_transactions))
            if len(all_transactions) > 0:
                for t in all_transactions:
                    print(t)
            else:
                print("No transactions for ZIP code {} in {}".format(zipcode, date))
        else:
            print('Your input is invalid. Try again')
        continue_inquiry = continue_method()

def transactions_type(self):
    continue_inquiry = True
    while (continue_inquiry):
        continue_inquiry = False #Prevents that it keeps asking once a result is delivered
        print(trans_menu_text2)
        trans_type = input()
        if (trans_type.isnumeric()):
            if (int(trans_type) in range(1,8)):
                query = """ SELECT COUNT(TRANSACTION_ID), SUM(TRANSACTION_VALUE)
                FROM CDW_SAPP_CREDIT_CARD
                WHERE TRANSACTION_TYPE = '{}'""".format(trans_type_dict[trans_type])
                db_cursor.execute(query)
                all_transactions = db_cursor.fetchall()
                if len(all_transactions) > 0:
                    print("Details of transactions of type {}".format(trans_type_dict[trans_type]))
                    print("Number of transactions: {}".format(all_transactions[0][0]))
                    print("Total value of transactions: $ {}".format(round(all_transactions[0][1], 2)))
                else:
                    print("No transactions")
            elif (trans_type == '9'):
                break
            elif (trans_type == '0'):
                global exit_flag
                exit_flag = True
                break
            else:
                print('Invalid option. Try again')
        else:
            print('another option {}'.format(trans_type))
        continue_inquiry = continue_method() #if a key is entered, we can keep checking
        print('there')

def transactions_state(self):
    print("here")
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
        for transaction in all_transactions:
            print(transaction)
        continue_inquiry = continue_method()

def customers_menu():
    cust = MenuBox(cust_menu_text, customers_show_details, do_nothing, customers_show_operations)
    cust.menu_box()

def customers_search(self, method):
    continue_inquiry = True
    while (continue_inquiry):
        continue_inquiry = False
        print(cust_menu_text1)
        lookup = input()
        if lookup == '1':
            print('Enter SSN:')
            ssn = input()
            method('cust.SSN', ssn, 'x')
        elif lookup == '2':
            print('Enter credit card number:')
            cred_card = input()
            method('cust.CREDIT_CARD_NO', cred_card, 'x')
        elif lookup == '3':
            print('Enter first name:')
            first_name = title_format(input()) #converts to title case format like in db
            print('Enter last name')
            last_name = title_format(input())
            method('cust.FIRST_NAME', first_name, last_name)
        elif lookup == '9':
            break
        elif lookup == '0':
            global exit_flag
            exit_flag = True
            break
        else:
            print('Invalid option. Try again')
            continue_inquiry = True


def customers_show_details(self):
    customers_search(self, customers_query_details)
    print("heeeelloooo")

    
def customers_query_details(sql_key, value1, value2):
    query = """ SELECT cust.FIRST_NAME, cust.LAST_NAME, cust.SSN, cust.CREDIT_CARD_NO
                FROM cdw_sapp_customer AS cust
                WHERE {} = '{}'""".format(sql_key, value1)
    if value2 != 'x': #If the search is by first and last name. We need to values
        query = query + " AND cust.LAST_NAME = '{}';".format(value2)
    db_cursor.execute(query)
    all_details = db_cursor.fetchall()
    if len(all_details) > 0:
        for d in all_details:
            print(d)



# def customers_update_details():

# def customers_monthly_bill():

def customers_show_operations(self):
    customers_search(self, customers_query_transactions)
    print('customers_show_operations')

def customers_query_transactions(sql_key, value1, value2):
    if (sql_key == 'cust.SSN' or sql_key == 'cust.CREDIT_CARD_NO'):
        identifier = value1
        # sql_key = 
        print("in the first if")
        print(sql_key)
    elif sql_key == 'cust.FIRST_NAME':
        print("another spot")
        subquery = """  SELECT CREDIT_CARD_NO
                        FROM cdw_sapp_customer AS cust
                        WHERE cust.FIRST_NAME = '{}' AND cust.LAST_NAME = '{}'""".format(value1, value2)
        db_cursor.execute(subquery)
        data = db_cursor.fetchone()
        sql_key = 'cust.CREDIT_CARD_NO' #so we can use one query statement for all
        if data is not None:
            identifier = data[0]
        else:
            identifier = ' '

    query = """ SELECT  cust.FIRST_NAME, cust.LAST_NAME, cust.CREDIT_CARD_NO, 
                        cred.TIMEID, cred.TRANSACTION_ID, cred.TRANSACTION_TYPE, cred.TRANSACTION_VALUE
                FROM cdw_sapp_customer AS cust
                INNER JOIN cdw_sapp_credit_card AS cred USING (CREDIT_CARD_NO)
                WHERE {} = '{}'""".format(sql_key, identifier)
    
    # if type == 1: #monthly bill
    #     print('Enter date (mm/yyyy):')
    #     date1 = input()
    #     query = query + "AND TIMEID = '{}'".format(date1+'05')
    # elif type == 2: #transactions between mm1/yyyy1 and mm2/yyyy2
    #     print('Enter starting date (mm/yyyy):')
    #     date1 = input()
    #     print('Enter ending date (mm/yyyy):')
    #     date2 = input()

    # print('Enter date (mm/yyyy):')
    # date1 = input()
    # query = query + "AND TIMEID = '{}'".format(date1[3:7]+ date1[0:2] + '05' )

    db_cursor.execute(query)
    print('second query')
    d = db_cursor.fetchall()
    if d is not None:
        for a in d:
            print(a)





    #         subquery = 
    # query = """ SELECT cust.FIRST_NAME, cust.LAST_NAME, .cust.CREDIT_CARD_NO, cred.TIMEID, cred.TRANSACTION_ID, cred.TRANSACTION_TYPE, cred.TRANSACTION_VALUE
    #             FROM cdw_sapp_customer AS cust
             #   INNER JOIN cdw_sapp_credit_card AS cred USING (CREDIT_CARD_NO)"""
    





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
            print("loans")
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