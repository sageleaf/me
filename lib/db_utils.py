import boto3
from boto3.dynamodb.conditions import Key
from lib.utils import generateUUID, generate_session_ticket
from datetime import datetime
from config import DB_TYPE, AWS_ACCESS_KEY_ID, AWS_REGION_NAME, AWS_SECRET_ACCESS_KEY, PRIVATE_KEY

db = boto3.resource(DB_TYPE, 
    region_name=AWS_REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

users_table = db.Table('users')

def db_get_user_record(authid):
    response = users_table.get_item(TableName='users', Key={ 'authid': authid })
    return response.get("Item")


def db_create_new_user(email, password, name, phone):
    authid=generateUUID()
    session_data  = generate_session_ticket()
    ticket = session_data.get("ticket")
    ticket_expires = session_data.get("expires")
    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item = {
        'authid': authid,
        'email': email,
        'password': password, 
        'name': name,
        'phone': phone,
        "ticket": ticket,
        "ticket_expires": ticket_expires,
        "create_date": create_date
    }
    users_table.put_item(Item=item)
    return db_get_user_record(authid)


def update_users_ticket(id):
    session_data  = generate_session_ticket()
    ticket = session_data.get("ticket")
    ticket_expires = session_data.get("expires")
    update_field(id=id, field="ticket", value=ticket)
    update_field(id=id, field="ticket_expires", value=ticket_expires)


def db_update_user_field(key, field, value):
   users_table.update_item(
    TableName="users",
    Key={ 'authid': key },
    UpdateExpression= "SET "+ field +" = :field_value",
    ExpressionAttributeValues={ 
        ":field_value": value
    })
 
def db_query_user_data(key, value):
    found_user = users_table.scan(
        ProjectionExpression=key,
        FilterExpression=Key(key).eq(value)
    )
    found_user_items = found_user["Items"]
    return found_user_items