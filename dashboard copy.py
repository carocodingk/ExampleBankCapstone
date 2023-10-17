import mysql.connector
import re

from mysql.connector import Error
from text_variables import welcome, continue_text, main_menu_text, trans_menu_text, trans_menu_text1, trans_menu_text2, trans_type_dict, trans_menu_text3, trans_states_dict
from text_variables import cust_menu_text, cust_menu_text1, cust_menu_text2, cust_update_dict
from data_transf import title_format
from secret import db_username, db_password

exit_flag = False

def do_nothing(self):
    pass

''' This function is a placeholder to generalize functions for 3 or parameters. In only prints invalid option 
    and then the loop continues until a valid option is entered. Menu_option is just a placeholder'''
def invalid_option(self, menu_option):
    print('Invalid option. Try again')

class MenuBox:
    def __init__(self, menu_msg, method1, method2, method3, method4):  #constructor
        self.menu_msg = menu_msg
        self.method1 = method1
        self.method2 = method2
        self.method3 = method3
        self.method4 = method4

    def menu_box(self):
        print("good morning")
        while(not exit_flag):         
            print(self.menu_msg)
            menu_option = input()
            print('you chose {}'.format(menu_option))
            if menu_option == '1':
                self.method1(self, menu_option)
            elif menu_option == '2':
                self.method2(self, menu_option)
            elif menu_option == '3':
                self.method3(self, menu_option)
            elif menu_option == '4':
                self.method4(self, menu_option)
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

def transactions_zipcode(self, placeholder):
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

def transactions_type(self, null):
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

def transactions_state(self, menu_option):
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
        for transaction in all_transactions:
            print(transaction)
        continue_inquiry = continue_method()

def customers_menu():
    cust = MenuBox(cust_menu_text, customers_show_details, customers_show_details, customers_show_operations, customers_show_operations)
    cust.menu_box()

def customers_search(self, menu_option, method):
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
            global exit_flag
            exit_flag = True
            break
        else:
            print('Invalid option. Try again')
            continue_inquiry = True


def customers_show_details(self, menu_option):
    customers_search(self, menu_option, customers_query_details)
    print("heeeelloooo")


#menu_option just a place_holder    
def customers_query_details(sql_key, value1, value2, menu_option):
    query = """ SELECT cust.FIRST_NAME, cust.LAST_NAME, cust.SSN, cust.CREDIT_CARD_NO
                FROM cdw_sapp_customer AS cust
                WHERE {} = '{}'""".format(sql_key, value1)
    if value2 != 'x': #If the search is by first and last name. We need to values
        query = query + " AND cust.LAST_NAME = '{}';".format(value2)
    db_cursor.execute(query)
    all_details = db_cursor.fetchall()
    if len(all_details) > 0:
        # for d in all_details:
        #     print(d)
        # print(all_details)
        (first_name, last_name, ssn, credit_card_no) = all_details[0]
        # print("heeere   {},{},{},{}".format(first_name, last_name, ssn, credit_card_no))
    
    if menu_option == '2': #update customer's details
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
            updated_data = updated_data[0:len(updated_data)-1]
            print(updated_data)
            # db_connection.start_transaction()
            # update = """UPDATE cdw_sapp_customer
            #             SET {}
            #             WHERE CREDIT_CARD_NO = '{}'""".format(updated_data, credit_card_no)
            update = """UPDATE cdw_sapp_customer
                        SET FIRST_NAME = 'JOSE'
                        WHERE CREDIT_CARD_NO = '123456100'"""
            print(update)
            db_cursor.execute(update)
            db_connection.commit()
            print('Data has been updated')
            #here we update the db and commit
        elif option == '9':
            break
        elif option == '0':
            global exit_flag
            exit_flag = True
            break #We don't use save_updates because we are not saving the changes. 
        else:
            print("Invalid option. Try again")




def customers_show_operations(self, menu_option):
    customers_search(self, menu_option, customers_query_transactions)
    print('customers_show_operations')

def customers_query_transactions(sql_key, value1, value2, menu_option):
    subquery = ""
    if (sql_key == 'cust.SSN'):
        subquery = """  SELECT CREDIT_CARD_NO
                        FROM cdw_sapp_customer 
                        WHERE SSN = '{}'""".format(value1)
    elif (sql_key == 'cust.CREDIT_CARD_NO'):
        identifier = value1
        sql_key = 'CREDIT_CARD_NO'
    elif sql_key == 'cust.FIRST_NAME':
        subquery = """  SELECT CREDIT_CARD_NO
                        FROM cdw_sapp_customer AS cust
                        WHERE cust.FIRST_NAME = '{}' AND cust.LAST_NAME = '{}'""".format(value1, value2)
        
    if len(subquery) > 0:
        db_cursor.execute(subquery)
        data = db_cursor.fetchone()
        sql_key = 'CREDIT_CARD_NO' #so we can use one query statement for all
        if data is not None:
            identifier = data[0]
        else:
            identifier = ' '
    print(identifier)

    #General query with some customer's details and transactions
    # query1 = """ SELECT  cust.FIRST_NAME, cust.LAST_NAME, cust.CREDIT_CARD_NO, 
    #                     cred.TIMEID, cred.TRANSACTION_ID, cred.TRANSACTION_TYPE, cred.TRANSACTION_VALUE
    #             FROM cdw_sapp_customer AS cust
    #             INNER JOIN cdw_sapp_credit_card AS cred USING (CREDIT_CARD_NO)
    #             WHERE {} = '{}'""".format(sql_key, identifier)
    query1 = """ SELECT cred.TIMEID, cred.TRANSACTION_ID, cred.TRANSACTION_TYPE, cred.TRANSACTION_VALUE
                FROM cdw_sapp_credit_card AS cred
                WHERE {} = '{}'""".format(sql_key, identifier)
    
    #Select specific month/year
    if menu_option == '3': #monthly bill
        print('Enter date (mm/yyyy):')
        date1 = input()
        date1 = date1[3:7]+date1[0:2] #Format as db
        query1 = query1 + "AND TIMEID like '{}%'".format(date1)
        # Add total and number of transactions
        query2 = """SELECT  cred.CREDIT_CARD_NO, cust.FIRST_NAME, MIDDLE_MAME, cust.LAST_NAME, cust.FULL_STREET_ADDRESS, cust.CUST_CITY, cust.CUST_STATE, cust.CUST_EMAIL,
                            COUNT(cred.TRANSACTION_ID), SUM(cred.TRANSACTION_VALUE)
                    FROM cdw_sapp_credit_card AS cred
                    INNER JOIN cdw_sapp_customer AS cust USING (CREDIT_CARD_NO)
                    WHERE {} = '{}' AND TIMEID like '{}%'
                    GROUP BY CREDIT_CARD_NO, FIRST_NAME, MIDDLE_MAME, LAST_NAME, cust.FULL_STREET_ADDRESS, cust.CUST_CITY, cust.CUST_STATE, cust.CUST_EMAIL""".format(sql_key, identifier, date1)
        print("at this other point")
        db_cursor.execute(query2)
        total_transactions = db_cursor.fetchall()
        if total_transactions is not None:
            print('count and total')
            for f in total_transactions:
                print(f)
    elif menu_option == '4': #transactions between mm1/yyyy1 and mm2/yyyy2
        print('Enter starting date (mm/yyyy):')
        date1 = input()
        date1 = int(date1[3:7]+date1[0:2]+'01')
        print('Enter ending date (mm/yyyy):')
        date2 = input()
        date2 = int(date2[3:7]+date2[0:2]+'31')
        print(date1, date2)
    
    print('breakpoint1')
    query1 = query1 + 'ORDER BY TIMEID DESC'
    db_cursor.execute(query1)
    all_transactions = db_cursor.fetchall()
    print('breakpoint2')

    if menu_option == '3':  #Monthly bill
        print('printing1')
        if all_transactions is not None:
            for t in all_transactions:
                print(t)
        print('printing2')
    elif menu_option == '4': #Transactions between dates
        if all_transactions is not None:
            for t in all_transactions:
                if (int(t[0]) >= date1 and int(t[0]) <= date2):
                    print(t[0] + '   ' + str(t[1]) + ' hhhhhhh ' + t[2] + str(t[3]))


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