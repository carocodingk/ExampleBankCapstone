import mysql.connector


from mysql.connector import Error
from text_variables import welcome, main_menu_text
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


class MenuBox:
    def __init__(self, menu_msg, msg1, msg2, msg3, method1, method2, method3): #constructor
        self.menu_msg = menu_msg
        self.msg1 = msg1
        self.msg2 = msg2
        self.msg3 = msg3
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
                self.method1(self.msg1)
            elif menu_option == '2':
                self.method2(self.msg2)
            elif menu_option == '3':
                self.method3(self.msg3)
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

# def transactions():





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
            print("transactions")
            m1 = MenuBox('hello',a,b,c,p1, p2, p3)
            m1.menu_box()
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