import boto3
from botocore.exceptions import ClientError
import json

# Define the table name and resource

table_name = 'music'
dynamodb = boto3.resource('dynamodb')
def create_music_table():

    # Check if the table already exists
    try:
        table = dynamodb.Table(table_name)
        table.table_status
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            # Table does not exist, so create it
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'title',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'artist',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'title',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'artist',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'year',
                        'AttributeType': 'N'
                    },
                    {
                        'AttributeName': 'web_url',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'image_url',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.wait_until_exists()
        else:
            # Some other error occurred, raise it
            raise e
    else:
        # Table exists, no need to create it
        print(f"Table {table_name} already exists.")

def load_music():
    table = dynamodb.Table(table_name)
    # Load data from a2.json
    with open('a2.json', 'r') as f:
        data = json.load(f)

    # Batch write the items to the table
    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)

    print(f"Data loaded into {table_name} table.")


