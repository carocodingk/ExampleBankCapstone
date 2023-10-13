welcome = """######################################################### 
##          WELCOME TO EXAMPLE BANK DASHBOARD          ## 
#########################################################"""

main_menu_text = """Please choose one of the following options:
(1) TRANSACTIONS
(2) CUSTOMERS
(3) LOANS
(0) EXIT"""

trans_menu_text = """Main > Transactions
    Choose one of the options for transactions:
        (1) Per zip code for mm/yyyy
        (2) Per type
        (3) Per state
        (9) Return to previous menu
        (0) Exit program"""

trans_menu_text1 = """_______________________________________________
Main > Transactions > By ZIPcode
Enter 9 to go back
Enter zip:"""

trans_menu_text2 = """_______________________________________________
Main > Transactions > By Type
Enter 9 to go back
Please choose a transaction type:
                (1) Bills
                (2) Education
                (3) Entertainment
                (4) Gas
                (5) Grocery
                (6) Healthcare
                (7) Test
                (9) Return to previous menu
                (0) Exit program"""


transactionTypeDict = {
    "1": "Bills",
    "2": "Education",
    "3": "Entertainment",
    "4": "Gas",
    "5": "Grocery",
    "6": "Healthcare",
    "7": "Test"
}