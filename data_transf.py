'''FUNCTION DEFINITIONS FOR DATA TRANSFORMATION'''
from tabulate import tabulate
# from text_variables import trans_type_dict, trans_states_dict

'''Reformats the phone number 1234567890 to (123)456-7890. 
If input is longer than 10 digits, it returns the first 10 digits. 
If input is shorter than 10 digits, it fills up with 0's at the beginning'''
def phone_format(phone):
    if type(phone) != str:
        phone = str(phone)
    if len(phone) < 10:
        phone = '0' * (10-len(phone)) + phone
    phone_num = '(' + phone[0:3] + ')' + phone[3:6] + '-' + phone[6:10]
    return(phone_num)

'''Converts the name or last name to title case.
input: mary / output: Mary 
input: MARY / output: Mary'''
def title_format(name):
    title_case = ''
    if not name[0].isupper() or not name[1:].islower():
        title_case = name[0].upper() + name[1:].lower()
    else:
        title_case = name
    return title_case

'''Adds a '0' in front of number under 10'''
def time_format(number):
    if number < 10:
        number = '0' + str(number)
    return number

'''For privacy: converts each character of a string to * except for the las 4 digits'''
def privacy_string(data_string):
    private_string = '*' * (len(data_string)-4) + data_string[-4:]
    return private_string

def print_zip_report(date, zip, transactions):
    print('\nTRANSACTIONS FOR ZIP CODE {} DURING {}'.format(zip, date))
    if len(transactions) > 0:
        header = ['Customer','Branch','Date','Transaction ID','Transaction Type','Amount']
        data = []
        for tr in transactions:
            customer = privacy_string(tr[0])    
            date = tr[2][4:6] + '/' + tr[2][0:2] + '/' + tr[2][0:4]
            amount = '$'+ str(tr[5])
            data.append([customer, tr[1], date, tr[3], tr[4], amount])
        print(tabulate(data, headers=header, tablefmt='pretty'))
    else:
        print('There are not transactions under this criteria\n')

def print_short_report(criteria, transactions):
    # if transactions is not None:
    print("##########################################")
    print("DETAILS OF TRANSACTIONS OF TYPE {}".format(criteria.upper()))
    print("------------------------------------------")
    print("Number of transactions: {}".format(transactions[0][0]))
    if transactions[0][1] is not None:
        print("Total value of transactions: ${}".format(round(transactions[0][1], 2)))
    else:
        print('Total value of transactions: $0')
        print("There are not transactions under this criteria")
    print("------------------------------------------")
    