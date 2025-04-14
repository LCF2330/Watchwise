import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('Users')

def validate_user(email, password):
    response = users_table.get_item(Key={'email': email})
    user = response.get('Item')
    if user and user['password'] == password:
        return True
    return False