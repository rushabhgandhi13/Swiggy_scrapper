from datetime import date, datetime
import requests
import json
import sys
from dateutil.relativedelta import relativedelta
import sqlite3
from sqlite3 import Error

HEADER = {
    'Host':'www.swiggy.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
    'Accept':'*/*',
    'Referer': 'https://www.swiggy.com/my-account/orders',
    'Content-Type': 'application/json'
    }

ORDER_LINK = 'https://www.swiggy.com/dapi/order/all?order_id='
db_file = 'swiggy.db'
conn = None
try:
    conn = sqlite3.connect(db_file)
except Error as e:
    print(e)

# Cookies are stored in a json file using cookie editor chrome extension
# Initially stored the cookies in a json file are now used in order to login to get the orders
print("Reading cookies from cookies.json")
data = None
cookies = {}
try:
    with open("cookies.json","r") as f:
        data = json.load(f)
except Exception as e:
    print("cookies.json not found in the path")
    print(str(e))

try:
    for i in data:
        cookies[i['name']] = i['value']
except Exception as e:
    print(str(e))
print("Cookies read successfully")

# Loggin Check(The user must be logged in to get the orders)
# First check if logged in
print("Checking if session is valid")
r = requests.get(ORDER_LINK, headers=HEADER, cookies=cookies)
response = None
try:
    response = json.loads(r.text)
except Exception as e:
    print(str(e))

if 'statusCode' not in response or 'data' not in response:
    print(str(e))

if response['statusCode'] == 1:
    print(str(e))
print("Session is valid")

# Get the orders

print("Getting orders...")
spent = 0
s = requests.Session()
last_order_id = ''
num_of_orders = 0
dishes = {}
# variables for 4 months
four_months = date.today() - relativedelta(months=+4)
four_amount = 0
four_amount_count = 0
while 1:
    URL = ''
    if last_order_id!='':
        URL = ORDER_LINK+str(last_order_id).strip()
    else:
        URL = ORDER_LINK

    r = s.get(URL, headers=HEADER, cookies=cookies)
    resp = json.loads(r.text)
    if resp['statusCode']==1:
        print("Status Code is 1, exiting")
        break

    if len(resp['data']['orders'])==0:
        break
    
    for order in resp['data']['orders']:
        order_id = order['order_id']
        order_total = order['order_total']
        order_date = str(order['order_time'])
        order_date = order_date[0:10]
        order_date = datetime.strptime(order_date, '%Y-%m-%d').date()
        if order_date > four_months:
            four_amount += order_total
            four_amount_count += 1
        num_of_orders+=1
        spent+=order_total
        items = order['order_items']

        with conn:
        # create a new order and storing it in the database
            order_data1 = (str(order_id), str(order_date), str(order_total), str(items))
            sql = """INSERT INTO sw_order (order_id,order_date,order_total,order_items)
                    VALUES (?,?,?,?)"""
            cur = conn.cursor()
            cur.execute(sql,order_data1)
            conn.commit()
        
        for item in items:
            name = item['name']
            if name in dishes:
                dishes[name] += 1
            else:
                dishes[name] = 1
    dishes={k: v for k, v in sorted(dishes.items(), key=lambda item: item[1], reverse=True)}
    most_ordered = list(dishes.keys())[0]
    number_of_orders = dishes[most_ordered]
    last_order_id = resp['data']['orders'][-1]['order_id']
average_spent = spent//num_of_orders
print("Order data stored in database successfully\n")
print()
print(f"The most ordered dish is  :  {most_ordered} \nThe number of orders for this dish is : {number_of_orders:,}\n")
print(f"Total money spent on swiggy.com in the last 4 months : Rs. {four_amount:,}")
print(f"Average money spent on swiggy.com in the last 4 months : Rs. {four_amount//four_amount_count:,}\n")
print(f"Total money spent on swiggy.com : Rs. {spent:,}")
print(f"Total number of orders placed : {num_of_orders:,}")
print(f"Average money spent on each order : Rs.{average_spent:,}")

# Writing the output to a file
f = open("A2_output.txt", "w")
f.write(f"The most ordered dish is  :  {most_ordered} \nThe number of orders for this dish is : {number_of_orders:,}\n")
f.write(f"Total money spent on swiggy.com in the last 4 months : Rs. {four_amount:,}\n")
f.write(f"Average money spent on swiggy.com in the last 4 months : Rs. {four_amount//four_amount_count:,}\n")
f.write(f"Total money spent on swiggy.com : Rs. {spent:,}\n")
f.write(f"Total number of orders placed : {num_of_orders:,}\n")
f.write(f"Average money spent on each order : Rs.{average_spent:,}\n")
f.close()

# order data is stored in swiggy.db