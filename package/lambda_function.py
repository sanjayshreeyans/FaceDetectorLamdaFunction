import boto3
import datetime
import gspread
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')


def push_to_sheet(studentname, filename):
    print("Reached push_to_sheet function")
    sa = gspread.service_account(filename='iep1-337004-678d886bff1c.json')

    sh = sa.open("Attendance Logs")

    wks = sh.worksheet("Sheet1")
    
    # Load date from date.txt

    dynamodb = boto3.resource('dynamodb')


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

    print(previousDate, "This is the previous date")
    
    # Print type
    print(type(previousDate), "This is the type of previousDate")
    

    # compare today's date with previousDate
    if datetime.datetime.now().date() > previousDate.date():
        print("The date is in the past")
        # Add 5 rows to the worksheet, at the top
        print("Adding 5 rows to the worksheet")
        for i in range(5):
            print("Entered for loop")
            if i == 3:
                wks.insert_row(["---- NEW DAY ----", ""], 2)
            else:
                wks.insert_row(["", ""], 2)
        # Update the dynamodb table with the new date
        print("Updating the dynamodb table with the new date")
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
        
        # table = dynamodb.Table('computerclassattendance')

        # response = table.put_item(Item={'studentname': 'mangatayi'})
        # status_code = response['ResponseMetadata']['HTTPStatusCode']
        # print(status_code)

        # Get ALL the attributes studentname from dyanamodb

        print("Scanning the dynamodb table for all the student names")
        table = dynamodb.Table('computerclassattendance')
        table_response = table.scan()
        table_data = table_response['Items']

    
        for item in table_data:
            name = item['studentname']
            wks.insert_row([name], 2)

        print(table_data)
        print("Created names in worksheet, new date ends here")
        


    # Insert the sign in
    print("Staring to insert the sign in")
    myfilename = filename

    # extract the name from the filename
    my_ms = int(myfilename.split(".")[0])

    print(my_ms)
    timezone = datetime.timezone(datetime.timedelta(hours=-4))


    my_datetime = datetime.datetime.fromtimestamp(
    my_ms / 1000, tz=timezone)  # Apply fromtimestamp function
    print(my_datetime)


    name = studentname


    print("Starting to determine the row number of the student")
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
    print("Starting to determine what period it is")

    print("Starting to perid1")
    if (my_datetime.time() >= datetime.time(8, 0)) and (my_datetime.time() <= datetime.time(10, 19)):
        print("Period 1")
        my_datetime = my_datetime.strftime("%d/%m/%Y %H:%M:%S")

        # Get all the values in the first column of the worksheet, from row 1 to row 30

        wks.update_cell(insertRow, 2, my_datetime)
        print("Ended period 1")

    # If the time is between 10:20 
    elif (my_datetime.time() >= datetime.time(10, 20)) and (my_datetime.time() <= datetime.time(11, 40)):
        print("Period 2")
        my_datetime = my_datetime.strftime("%d/%m/%Y %H:%M:%S")
        # insert the second parameter at the 3rd collum
        wks.update_cell(insertRow, 3, my_datetime)

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
        
        
def lambda_handler(event, context):
    # Get the object from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(key, type(key))
    # Use Rekognition to detect faces in the uploaded image
    response = rekognition.search_faces_by_image(
        CollectionId='doc-example-collection-demo',
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        },
        FaceMatchThreshold=80,
        MaxFaces=10,
    )

    # If any faces are found, print their external IDs
    if len(response['FaceMatches']) > 0:
        for face_match in response['FaceMatches']:
            external_image_id = face_match['Face']['ExternalImageId']
            print(
                f"Face found with external ID {external_image_id} in image {key}")
            print("Updating the spreadsheet")
            push_to_sheet(external_image_id, key)
            print("Done, returned to lambda_handler")
            
            

            

