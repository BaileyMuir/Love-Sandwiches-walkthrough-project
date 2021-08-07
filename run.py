# python code goes here
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    get sales figures input the user.
    Run a while loop to collect valid string of data from the user
    Via the terminal, which must be a string of 6 numbers seperated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("please eneter sales data from last market.")
        print("data should be six numbers, seperated by commas")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("enter your data here: ")
    
        sales_data = data_str.split(",")
    
        if validate_data(sales_data):
            print("data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    inside the try, converts all string values into intergers.
    Raises ValueErroe if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        {int(value) for value in values}
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid daya: {e}, please try again.\n")
        return False

    return True

# def update_sales_worksheet(data):
#     """
#     update sales worksheet, add new row with the list data provided.
#     """

#     print("updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("sales worksheet updated successfully.\n")

# def update_surplus_worksheet(data):
#     """
#     update surplus worksheet, add new row with the list data provided.
#     """

#     print("updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet):
    """
    Recives a list of intergers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """

    print(f"updating {worksheet} worksheet.....\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figures subtracked from the stock:
    - positive surplus indicates waste.
    - Negative surplus indicates extra was made when stoock was sold out.
    """

    print("Calculating surplus data....\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def get_last_5_entries_sales():
    """
    Collects collumns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """

    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

print("Welcome to love sandwiches Data Automation")
# main()

sales_columns = get_last_5_entries_sales()