import boto3

# Initialize the Rekognition client

rekognition = boto3.client(
    'rekognition', aws_access_key_id='AKIA5KTQWF6JJLZC35MX', aws_secret_access_key='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', region_name="us-east-1")
# Load the detected face image from file
with open("face.jpg", "rb") as f:
    face_image = f.read()

# Perform liveness  detection on the face image

response = rekognition.detect_(
    Image={"Bytes": face_image},
    CollectionId="my-collection",
)

# Check the authentication result
score = response["AuthenticationResult"]["Score"]
if score > 0.9:
    print("Face is from a live human being")
else:
    print("Face is from a static image")
