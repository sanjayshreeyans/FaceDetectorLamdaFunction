
import gspread
import datetime
import boto3
from itertools import groupby

sa = gspread.service_account(filename='iep1-337004-678d886bff1c.json')

sh = sa.open("Attendance Logs")

wks = sh.worksheet("Sheet1")

dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                              aws_access_key_id='AKIA5KTQWF6JJLZC35MX', aws_secret_access_key='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')
    

# Load date from date.txt

table1 = dynamodb.Table('dateStorage')

# Get the item with partition key value of "1"
response1 = table1.get_item(
    Key={
        'num': '1'
    }
)

# Get the value of the "date" attribute from the item
previousDate = response1['Item']['date']

previousDate = datetime.datetime.strptime(previousDate, "%m/%d/%Y")

# comapre today's date with previousDate
if datetime.datetime.now().date() > previousDate.date():
    print("The date is in the past")
    # Add 5 rows to the worksheet, at the top
    for i in range(5):
        if i == 3:
            wks.insert_row(["---- NEW DAY ----", ""], 2)
        else:
            wks.insert_row(["", ""], 2)
    
    
    table1.update_item(
    Key={
        'num': '1'
    },
    UpdateExpression='SET #attrName = :attrValue',
    ExpressionAttributeNames={
        '#attrName': 'date'
    },
    ExpressionAttributeValues={
        ':attrValue': (datetime.datetime.now().strftime("%m/%d/%Y"))
    }
)
    
    print("The date has been updated to", (datetime.datetime.now().strftime("%m/%d/%Y")))
        
        
        
    # dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                            #   aws_access_key_id='AKIA5KTQWF6JJLZC35MX', aws_secret_access_key='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')
    # table = dynamodb.Table('computerclassattendance')
    
    # response = table.put_item(Item={'studentname': 'mangatayi'})
    # status_code = response['ResponseMetadata']['HTTPStatusCode']
    # print(status_code)
    
    # Get ALL the attributes studentname from dyanamodb
    
    table = dynamodb.Table('computerclassattendance')
    table_response = table.scan()
    table_data = table_response['Items']
    
    for item in table_data:
        name = item['studentname']
        wks.insert_row([name], 2)

    print(table_data)
    
    
# Insert the sign in
myfilename = "1679250396721.png"

# extract the name from the filename
my_ms = int(myfilename.split(".")[0])

print(my_ms)

timezone = datetime.timezone(datetime.timedelta(hours=-4))

my_datetime = datetime.datetime.fromtimestamp(
    my_ms / 1000, tz=timezone)  # Apply fromtimestamp function
print(my_datetime)


name = 'sanjay'


# Code to determine the row number of the student
wks_values = wks.col_values(1)

# Split the list by the value of '---- NEW DAY ----'
separator = '---- NEW DAY ----'

sublists = []
temp_list = []
for item in wks_values:
    if item == separator:
        sublists.append(temp_list)
        temp_list = []
    else:
        temp_list.append(item)
sublists.append(temp_list)


todaysList = sublists[0]

insertRow = (todaysList.index(name))+1
# End of code to determine the row number of the student

print(insertRow, "This is the row number of the student")


# Determine what period it is, this will determine the collum in the worksheet

# if the time is between 8:00 AM and 10:19 AM, it is period 1

if (my_datetime.time() >= datetime.time(8, 0)) and (my_datetime.time() <= datetime.time(10, 19)):
    print("Period 1")
    my_datetime = my_datetime.strftime("%d/%m/%Y %H:%M:%S")
    
    # Get all the values in the first column of the worksheet, from row 1 to row 30
    
    wks.update_cell(insertRow, 2, my_datetime)

# If the time is between 10:20 AM and 11:40 PM, it is period 2
elif (my_datetime.time() >= datetime.time(10, 20)) and (my_datetime.time() <= datetime.time(11, 40)):
    print("Period 2")
    my_datetime = my_datetime.strftime("%d/%m/%Y %H:%M:%S")
    # insert the second parameter at the 3rd collum
    wks.update_cell(insertRow, 3, my_datetime)


# IF the time is between 12:20 PM and 1:55 PM, it is period 3
elif (my_datetime.time() >= datetime.time(12, 20)) and (my_datetime.time() <= datetime.time(13, 55)):
    print("Period 3")
    my_datetime = my_datetime.strftime("%d/%m/%Y %H:%M:%S")
    # insert the second parameter at the 4th collum
    wks.update_cell(insertRow, 4, my_datetime)


# IF the time is between 1:56 PM and 3:15 PM,
elif (my_datetime.time() >= datetime.time(13, 56)) and (my_datetime.time() <= datetime.time(15, 15)):
    print("Period 4")
    my_datetime = my_datetime.strftime("%d/%m/%Y %H:%M:%S")
    # insert the second parameter at the 5th collum
    wks.update_cell(insertRow, 5, my_datetime)
    

else:
    print("After school")