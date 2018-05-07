from lib.db_utils import db_get_user_record, db_create_new_user, db_update_user_field, db_query_user_data
from lib.utils import verify_password, validate_ticket


class User:
    def __init__( self, email, password, name, phone, authid):
        self.email = email
        self.password = password
        self.name = name
        self.phone = phone
        self.authid = authid
        self.validated = False
        
    def search_for_user_by(self, key, value):
        found_user = db_query_user_data(key, value)
        return found_user

    def create_new_user(self):
        new_user = db_create_new_user(self.email, self.password, self.name, self.phone)
        return new_user

    def get_user_from_store(self):
        user = db_get_user_record(authid=self.authid)
        return user
        
    def update_user_in_store(self):
        user = self.get_user_from_store()
        authid = user.get("authid")
        updated_user = put_user_data(self.email, self.password, authid)
        return updated_user
    
    def validate_user_ticket(self, ticket):
        user = self.get_user_from_store()
        ticket_in_db = user.get("ticket")
        ticket_expires = user.get("ticket_expires")
        self.validated = validate_ticket(ticket, ticket_in_db, ticket_expires)
        return self.validated 

    def validate_user_password(self, password):
        user = self.get_user_from_store()
        if user is None:
            self.password_valid = False
            return self.password_valid
        authid          = user.get("authid")
        stored_password = user.get("password")
        self.password_valid  = verify_password(password, stored_password)
        return self.password_valid



