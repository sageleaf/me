from lib.utils import generateUUID, generate_session_ticket, db

users_table = db.Table('users')

def get_user_record(email):
    response = users_table.get_item(TableName='users', Key={ 'email': email })
    return response.get("Item")


def put_user_data(email, password, authid=generateUUID()):
    session_data  = generate_session_ticket()
    ticket = session_data.get("ticket")
    ticket_expires = session_data.get("expires")
    item = {
                'authid': authid,
                'email': email,
                'password': password, 
                'ticket': ticket,
                'ticket_expires': ticket_expires
            }

    users_table.put_item(Item=item)
    return item