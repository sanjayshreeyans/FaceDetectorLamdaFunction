import boto3

# Initialize Rekognition client
rekognition_client = boto3.client('rekognition', region_name='us-east-1',
                              aws_access_key_id='AKIA5KTQWF6JJLZC35MX', aws_secret_access_key='GxW9L2zYoaOiS8VCf9gAEdU6Yr59/7u4IoVsiF6V')

# Set collection ID
collection_id = 'doc-example-collection-demo'

# List all faces in collection
response = rekognition_client.list_faces(CollectionId=collection_id)

# Print face details
for face in response['Faces']:
    print(f"Face ID: {face['FaceId']}")
    print(f"External Image ID: {face['ExternalImageId']}")
    print(f"Image ID: {face['ImageId']}")
    print(f"Confidence: {face['Confidence']}")
