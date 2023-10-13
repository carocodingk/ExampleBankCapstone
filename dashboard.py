import mysql.connector
import re

from mysql.connector import Error
from text_variables import welcome, main_menu_text, trans_menu_text, trans_menu_text1, trans_menu_text2
from secret import db_username, db_password

exit_flag = False

a = "text1"
b = 'text2'
c = 'text3'

def p1(t):
    print('1 ' + t)

def p2(t):
    print('2 ' + t)

def p3(t):
    print('3 ' + t)

def do_nothing(self):
    pass


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
                self.method1('A')
            elif menu_option == '2':
                self.method2('B')
            elif menu_option == '3':
                self.method3('C')
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

def transactions_menu():
    tr = MenuBox(trans_menu_text, transactions_zipcode, transactions_type, p3)
    tr.menu_box()

def transactions_zipcode(self):
    zipcode = '0000' #initial value to enter in loop
    date = '01/1234'

    while (True):
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
    # print(welcome)
    while (not exit_flag):
        print(welcome)
        print(main_menu_text)
        main_menu_option = input()
        if main_menu_option == '1':
            # print("transactions")
            # m1 = MenuBox('hello',a,b,c,p1, p2, p3)
            transactions_menu()
        elif main_menu_option == '2':
            print("customers")
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