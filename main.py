import boto3
import json
from datetime import datetime

sqs = boto3.client('sqs', region_name='us-east-1')

# Initialize S3 client
s3 = boto3.client('s3', region_name='us-east-1')
bucket_name = 'lior-bucket-devops'  # Replace 'your-bucket-name' with your S3 bucket name

def receive_message_from_sqs(queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20 
    )
    
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        
        return message['Body']
    else:
        return None

def upload_to_s3(content):
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{timestamp}.txt'
    
    # Upload content to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=filename,
        Body=content.encode('utf-8')  # Assuming content is in UTF-8 format
    )
    
    print(f'Message saved to S3 with filename: {filename}')

def main():
    queue_url = 'https://sqs.us-east-1.amazonaws.com/637423594714/liorQueue'
    
    # Receive message from SQS
    message = receive_message_from_sqs(queue_url)
    
    if message:
        # Upload message content to S3
        upload_to_s3(message)
    else:
        print('No messages available in SQS queue.')

if __name__ == '__main__':
    main()