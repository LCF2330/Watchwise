import boto3
from boto3.dynamodb.conditions import Key
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION", "us-east-1")

dynamodb = boto3.resource(
    'dynamodb',
    region_name=aws_region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

table = dynamodb.Table('Watchlist')

def get_items(user_id):
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    return response['Items']

def get_item(user_id, title):
    response = table.get_item(
        Key={'user_id': user_id, 'title': title}
    )
    return response.get('Item')

def add_item(user_id, title, genre, rating, watched=False):
    table.put_item(
        Item={
            'user_id': user_id,
            'title': title,
            'genre': genre,
            'rating': rating,
            'watched': watched
        }
    )

def update_item(user_id, old_title, new_title, genre, rating, watched):
    if old_title != new_title:
        delete_item(user_id, old_title)
        add_item(user_id, new_title, genre, rating, watched)
    else:
        table.update_item(
            Key={'user_id': user_id, 'title': old_title},
            UpdateExpression="SET genre = :g, rating = :r, watched = :w",
            ExpressionAttributeValues={
                ':g': genre,
                ':r': rating,
                ':w': watched
            }
        )

def delete_item(user_id, title):
    table.delete_item(
        Key={'user_id': user_id, 'title': title}
    )
