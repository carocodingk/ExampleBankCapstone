'''FUNCTION DEFINITIONS FOR DATA TRANSFORMATION'''

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