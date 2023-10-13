welcome = """######################################################### 
##          WELCOME TO EXAMPLE BANK DASHBOARD          ## 
#########################################################"""

main_menu_text = """_______________________________________________
Please choose one of the following options:
(1) TRANSACTIONS
(2) CUSTOMERS
(3) LOANS
(0) EXIT"""

trans_menu_text = """_______________________________________________
Main > Transactions
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


trans_type_dict = {
    "1": "Bills",
    "2": "Education",
    "3": "Entertainment",
    "4": "Gas",
    "5": "Grocery",
    "6": "Healthcare",
    "7": "Test"
}

trans_menu_text3 = """_______________________________________________
Main > Transactions > By State
Please enter a state:
"""

statesDict = {
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