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

"""sales = SHEET.worksheet('sales')
data = sales.get_all_values()
print(data)"""

def get_sales_data():
    """
    Get sales figures input from user
    Run a while loop to cllect a valid string data frrom the user
    via the terminal, which must be a string of 6 numbers seprated by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, spreated by commas.")
        print("Example: 10,20,30,40,50,60\n")
        data_str= input("Enter your data here: ")
        sales_data=data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data    

    


def validate_data(values):
    """
    Inside the try, converts all string values into integers
    Raises ValueError if strings cannot be converted into int
    or if there arn't exactly 6 values.
    """

    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f"Exactly 6 values required you provides {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e},please try again.\n")
        return False
    return True

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each type.
    The surplus is defined as sales fugure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data..\n")
    stock=SHEET.worksheet("stock").get_all_values()
    stock_row=stock.pop() #or I can use stock[-1]

    surplus_data = []
    for stock,sales in zip(stock_row,sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data 

def update_worksheet(data,worksheet):
    """
    Receive a list of integers to be inserted into a worksheet
    Update the relevant worksheet with data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n") 

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and return the data as a list os lists
    """ 
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns    
def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column)/len(int_column) #len(int_column) = 5
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data

def get_stock_values(data):
    """
    Built the code to calculate and insert our recommended stock values into the stock worksheet. 
    In this challenge you will build a dictionary, 
    where the keys are the sandwich headings pulled from the spreadsheet,
    and the values are the calculated stock data.
    """
    sales = SHEET.worksheet("sales").get_all_values()

    headings = sales.pop(0)
    my_dict = {}
    for head,stock in zip(headings,data):
        my_dict[head]=stock
    return my_dict  
def main():
    """
    Run alll program function
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data] 
    update_worksheet(sales_data,"sales") 
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,"surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    stock_values = get_stock_values(stock_data)
    print("Make the following numbers of sandwiches for next market:\n")
    print(stock_values)

print("Welcom to Love Sandwich Data Atuomation")    
main()   
