import boto3
from botocore.exceptions import ClientError
import json
from decimal import Decimal

# Define the table name and resource

table_name = 'music'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


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
                        'AttributeName': 'artist',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'year',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'artist',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'year',
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
    # Load data from music.json
    with open("/var/www/myapp/music.json") as json_file:
        music_list = json.load(json_file, parse_float=Decimal)
        print(music_list)

    for music in music_list:
        artist = music['artist']
        year = int(music['year'])
        title = music['title']
        web_url = music['web_url']
        img_url = music['img_url']
        table.put_item(Item=music)

    print(f"Data loaded into {table_name} table.")
