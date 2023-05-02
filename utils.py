import boto3
from botocore.exceptions import ClientError
import json

from main import app


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


def create_login_table():
    # Check if the table already exists
    try:
        table = dynamodb.Table('login')
        table.table_status
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            # Table does not exist, so create it
            table = dynamodb.create_table(
                TableName='login',
                KeySchema=[
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'email',
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
        print(f"Table login already exists.")


def load_login_data():
    table = dynamodb.Table('login')
    items = [
        {
            'email': 's34252420@student.rmit.edu.au',
            'user_name': 'Bai Lin Johannes Ao0',
            'password': '012345'
        },
        {
            'email': 's34252421@student.rmit.edu.au',
            'user_name': 'Bai Lin Johannes Ao1',
            'password': '123456'
        },
        {
            'email': 's34252422@student.rmit.edu.au',
            'user_name': 'Bai Lin Johannes Ao2',
            'password': '234567'
        },
        {
            'email': 's34252423@student.rmit.edu.au',
            'user_name': 'Bai Lin Johannes Ao3',
            'password': '345678'
        },
        {
            'email': 's34252424@student.rmit.edu.au',
            'user_name': 'Bai Lin Johannes Ao4',
            'password': '456789'
        },
        {
            'email': 's34252425@student.rmit.edu.au',
            'user_name': 'Bai Lin Johannes Ao5',
            'password': '567890'
        },
        {
            'email': 's34252426@student.rmit.edu.au',
            'user_name': 'Bai Lin Johannes Ao6',
            'password': '678901'
        },
        {
            'email': 's34252427@student.rmit.edu.au',
            'user_name': 'Bai Lin Johannes Ao7',
            'password': '789012'
        },
        {
            'email': 's34252428@student.rmit.edu.au',
            'user_name': 'Bai Lin Johannes Ao8',
            'password': '890123'
        },
        {
            'email': 's34252429@student.rmit.edu.au',
            'user_name': 'Bai Lin Johannes Ao9',
            'password': '901234'
        }
    ]

    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)



def create_music_table():
    table_name = 'music'
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
                        'AttributeName': 'title',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'artist',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'title',
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
    table_name = 'music'
    table = dynamodb.Table(table_name)
    # Load data from music.json
    with open("/var/www/myapp/music.json") as json_file:
        data = json.load(json_file)

    songs = data['songs']
    for song in songs:
        artist = song['artist']
        year = int(song['year'])
        title = song['title']
        web_url = song['web_url']
        img_url = song['img_url']
        table.put_item(Item=song)

    print(f"Data loaded into {table_name} table.")


def validate_user(email, password):
    login_table = dynamodb.Table('login')

    try:
        response = login_table.get_item(
            Key={
                'email': email
            }
        )
    except ClientError as e:
        app.logger.info(e.response['error']['message'])
        return False

    else:
        # check if response contains item and password matches
        if 'Item' in response and response['Item']['password'] == password:
            return response['Item']
        else:
            return False

def is_email_exist(email):
    table = dynamodb.Table('login')
    response = table.get_item(Key={'email': email})
    if 'Item' in response:
        return True
    return False

def insert_user(email, username, password):
    table = dynamodb.Table('login')
    table.put_item(Item={'email': email, 'user_name': username, 'password': password})


