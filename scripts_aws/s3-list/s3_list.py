import boto3 


def lambda_handler(event, context):
    
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()
 
    #print(response.get('Buckets'))
    
    for bucket in response.get('Buckets'):
        print('Name: {0} - Creation Date: {1}'.format(
            bucket['Name'],
            bucket['CreationDate']
            )
        )
   
lambda_handler({}, {})