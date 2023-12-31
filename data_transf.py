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
    print("DETAILS OF TRANSACTIONS FOR {}".format(criteria.upper()))
    print("------------------------------------------")
    print("Number of transactions: {}".format(transactions[0][0]))
    if transactions[0][1] is not None:
        print("Total value of transactions: ${}".format(round(transactions[0][1], 2)))
    else:
        print('Total value of transactions: $0')
        print("There are not transactions under this criteria")
    print("------------------------------------------")


def print_monthly_bill(date, bill_summary, all_transactions):
    if bill_summary is not None:
        print("##########################################")
        text = "\nClient: {} {} {} \n".format(bill_summary[1], bill_summary[2], bill_summary[3])
        text = text + "Address: {}, {}, {}, {}, {} \n".format(bill_summary[4], bill_summary[5], bill_summary[6], bill_summary[7], bill_summary[8])
        text = text + "Email: {} \n".format(bill_summary[9])
        text = text + "Account: {} \n\n".format(privacy_string(bill_summary[0]))
        text = text + "         MONTHLY BILL FOR {} \n".format(date)
        trans = []
        header = ['Date', 'Trans. ID', 'Description', 'Amount ($)']
        text1 = "\nNumber of transactions: {} \n".format(bill_summary[10])
        text1 = text1 + "Total: ${}".format(bill_summary[11 ])
        for tr in all_transactions:
            date = tr[0][4:6] + '/' + tr[0][6:] + '/' + tr[0][0:2]
            trans.append([date, tr[1], tr[2], round(tr[3],2)])
        print(text)
        print(tabulate(trans, headers=header, tablefmt='pretty'))
        print(text1)
        print('\n>>>>> Success! Your monthly bill has been generated')
    else:
        print('This account does not exist in our database')
    print("------------------------------------------")

def print_monthly_bill1(date, bill_summary, all_transactions):
    
    if bill_summary is not None:
        print("Enter a name for the file without spaces or special characters: (no need to add extension)")
        filename = input()
        with open(filename + '.txt', 'w') as new_file:
            new_file.write("##########################################")
            text = "\nClient: {} {} {} \n".format(bill_summary[1], bill_summary[2], bill_summary[3])
            text = text + "Address: {}, {}, {}, {}, {} \n".format(bill_summary[4], bill_summary[5], bill_summary[6], bill_summary[7], bill_summary[8])
            text = text + "Email: {} \n".format(bill_summary[9])
            text = text + "Account: {} \n\n".format(privacy_string(bill_summary[0]))
            text = text + "         MONTHLY BILL FOR {} \n".format(date)
            trans = []
            header = ['Date', 'Trans. ID', 'Description', 'Amount ($)']
            text1 = "\nNumber of transactions: {} \n".format(bill_summary[10])
            text1 = text1 + "Total: ${}".format(round(bill_summary[11 ],2))
            for tr in all_transactions:
                date = tr[0][4:6] + '/' + tr[0][6:] + '/' + tr[0][0:2]
                trans.append([date, tr[1], tr[2], round(tr[3],2)])
            new_file.write(text)
            new_file.write(tabulate(trans, headers=header, tablefmt='pretty'))
            new_file.write(text1)
            new_file.write("\n------------------------------------------")
        print('\n>>>>> Success! Your monthly bill has been printed')
            

def print_transactions(date1, date2, dates, customer_info, identifier, all_transactions):
    if customer_info is not None and all_transactions is not None:
        print("\n##########################################")
        text = "\nClient: {} {} {}\n".format(customer_info[0], customer_info[1], customer_info[2])
        text = text + "Acount: {} \n\n".format(privacy_string(identifier))
        text = text + "       TRANSACTIONS BETWEEN {} AND {}\n".format(dates[0], dates[1])
        trans = []
        header = ['Date', 'Trans. ID', 'Description', 'Amount ($)']
        for tr in all_transactions:
            if (int(tr[0]) >= date1 and int(tr[0]) <= date2): #filtering by dates
                date = tr[0][4:6] + '/' + tr[0][6:] + '/' + tr[0][0:2]
                trans.append([date, tr[1], tr[2], round(tr[3],2)])
        print(text)
        if len(trans) > 0:
            print(tabulate(trans, headers=header, tablefmt='pretty'))   
        else:     
            print("There are not transactions under this criteria")
    elif customer_info is None:
        print('This account does not exist in our database')
    print("------------------------------------------")


def print_customer_details(all_details):
    print("##########################################")
    print("DETAILS OF TRANSACTIONS OF CUSTOMER")
    print("------------------------------------------")
    text = "\nClient: {} {} {} \n".format(all_details[1], all_details[2], all_details[3])
    text = text + "SSN: {}\n".format(privacy_string(str(all_details[0])))
    text = text + "Address: {}, {}, {}, {}, {}\n".format(all_details[5], all_details[6], all_details[7], all_details[8], all_details[9])
    text = text + "Phone: {}\n".format(all_details[10])
    text = text + "Email: {}\n".format(all_details[11])
    text = text + "Account: {}\n".format(all_details[4])
    print(text)
    print("------------------------------------------")
