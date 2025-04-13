import os
import boto3
from dotenv import load_dotenv
from boto3.dynamodb.conditions import Key

# Load environment variables
load_dotenv()

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Access the table
table = dynamodb.Table(os.getenv('DYNAMO_TABLE_NAME'))

def get_items(user_id):
    """Retrieve all items for a specific user from the watchlist."""
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    return response.get('Items', [])

def add_item(user_id, item_id, title, genre, rating):
    """Add a new item to the user's watchlist."""
    table.put_item(
        Item={
            'user_id': user_id,
            'item_id': item_id,
            'title': title,
            'genre': genre,
            'rating': rating
        }
    )
