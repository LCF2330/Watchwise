import boto3
from boto3.dynamodb.conditions import Key

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Watchlist') 

def get_items(user_id):
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    return response['Items']

def get_item(user_id, title):
    response = table.get_item(
        Key={
            'user_id': user_id,
            'title': title
        }
    )
    return response.get('Item')

def add_item(user_id, title, genre, rating, watched=False, review=""):
    table.put_item(
        Item={
            'user_id': user_id,
            'title': title,
            'genre': genre,
            'rating': rating,
            'watched': watched,
            'review': review  
        }
    )

def update_item(user_id, old_title, new_title, genre, rating, watched, review):
    if old_title != new_title:
        delete_item(user_id, old_title)
        add_item(user_id, new_title, genre, rating, watched, review)
    else:
        table.update_item(
            Key={
                'user_id': user_id,
                'title': old_title
            },
            UpdateExpression="SET genre = :g, rating = :r, watched = :w, review = :v",
            ExpressionAttributeValues={
                ':g': genre,
                ':r': rating,
                ':w': watched,
                ':v': review  
            }
        )

def delete_item(user_id, title):
    table.delete_item(
        Key={
            'user_id': user_id,
            'title': title
        }
    )
