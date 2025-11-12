import boto3

s3 = boto3.client('s3')

url = s3.generate_presigned_url(
    'put_object',
    Params={'Bucket': 'mahinraza', 'Key': 'README.md'},
    ExpiresIn=3600
)

print("Download URL:", url)