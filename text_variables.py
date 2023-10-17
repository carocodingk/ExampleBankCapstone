welcome = """######################################################### 
##          WELCOME TO EXAMPLE BANK DASHBOARD          ## 
#########################################################"""

continue_text = """Press   (9) Return to previous menu
        (0) Exit program
        Any other key to continue"""

main_menu_text = """__________________________________________________________
Please choose one of the following options:
(1) TRANSACTIONS
(2) CUSTOMERS
(3) LOANS
(0) EXIT"""

trans_menu_text = """__________________________________________________________
Main > Transactions
    Choose one of the options to see transactions:
        (1) Per zip code for mm/yyyy
        (2) Per type
        (3) Per state
        (9) Return to previous menu
        (0) Exit program"""

trans_menu_text1 = """__________________________________________________________
Main > Transactions > By ZIPcode
Enter 9 to go back
Enter zip:"""

trans_menu_text2 = """__________________________________________________________
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


trans_type_dict = {
    "1": "Bills",
    "2": "Education",
    "3": "Entertainment",
    "4": "Gas",
    "5": "Grocery",
    "6": "Healthcare",
    "7": "Test"
}

trans_menu_text3 = """__________________________________________________________
Main > Transactions > By State
Please enter a state:"""

trans_states_dict = {
    "ALABAMA": "AL",
    "ALASKA": "AK",
    "ARIZONA": "AZ",
    "ARKANSAS": "AR",
    "CALIFORNIA": "CA",
    "COLORADO": "CO",
    "CONNECTICUT": "CT",
    "DELAWARE": "DE",
    "DISTRICT OF COLUMBIA": "DC",
    "FLORIDA": "FL",
    "GEORGIA": "GA",
    "HAWAII": "HI",
    "IDAHO": "ID",
    "ILLINOIS": "IL",
    "INDIANA": "IN",
    "IOWA": "IA",
    "KANSAS": "KS",
    "KENTUCKY": "KY",
    "LOUISIANA": "LA",
    "MAINE": "ME",
    "MARYLAND": "MD",
    "MASSACHUSETTS": "MA",
    "MICHIGAN": "MI", 
    "MINNESOTA": "MN",
    "MISSISSIPPI": "MS",
    "MISSOURI": "MO",
    "MONTANA": "MT",
    "NEBRASKA": "NE",
    "NEVADA": "NV",
    "NEW HAMPSHIRE": "NH",
    "NEW JERSEY": "NJ",
    "NEW MEXICO": "NM",
    "NEW YORK": "NY",
    "NORTH CAROLINA": "NC",
    "NORTH DAKOTA": "ND",
    "OHIO": "OH",
    "OKLAHOMA": "OK",
    "OREGON": "OR",
    "PENNSYLVANIA": "PA",
    "RHODE ISLAND": "RI",
    "SOUTH CAROLINA": "SC",
    "TENNESSEE": "TN",
    "TEXAS": "TX",
    "UTAH": "UT",
    "VERMONT": "VT",
    "VIRGINIA": "VA",
    "WASHINGTON": "WA",
    "WEST VIRGINIA": "WV",
    "WISCONSIN": "WI",
    "WYOMING": "WY"
}

cust_menu_text = """__________________________________________________________
Main > Customers
    Choose one of the options for customers:
        (1) Show customer's details
        (2) Modify customer's details
        (3) Show monthly bill for customer
        (4) Show customer's transactions
        (9) Return to previous menu
        (0) Exit program"""

cust_menu_text1 = """__________________________________________________________
Main > Customers
    Lookup customer by:
            (1) By SSN
            (2) By credit card number
            (3) By name
            (9) Return to previous menu
            (0) Exit program"""

cust_menu_text2 = """__________________________________________________________
Main > Customers > Update custommer
Choose the field to update:
                (1A) First name
                (1B) Middle name
                (1C) Last name
                (2A) Full street address
                (2B) City
                (2C) State
                (2D) ZIP
                (3A) Phone
                (3B) Email
                (8)  Finish with updates
                (9)  Cancel and go back to previos menu
                (0)  Exit program without saving updates"""

cust_update_dict = {
    "1A": "FIRST_NAME",
    "1B": "MIDDLE_NAME",
    "1C": "LAST_NAME",
    "2A": "FULL_STREET_ADDRESS",
    "2B": "CUST_CITY",
    "2C": "CUST_STATE",
    "2D": "CUST_ZIP",
    "3A": "CUST_PHONE",
    "3B": "CUST_EMAIL"
}


