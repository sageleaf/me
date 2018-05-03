from lib.db_utils import get_user_record, put_user_data
from lib.utils import verify_password, validate_ticket


class User:
    def __init__( self, email, password=None):
        self.email = email
        self.password = password
        self.validated = False

    def get_user_from_store(self):
        user = get_user_record(email=self.email)
        return user
        
    def update_store(self):
        user = self.get_user_from_store()
        authid = user.get("authid")
        updated_user = put_user_data(self.email, self.password, authid)
        return updated_user
    
    def validate_ticket(self, ticket):
        user = self.get_user_from_store()
        ticket_in_db = user.get("ticket")
        ticket_expires = user.get("ticket_expires")
        self.validated = validate_ticket(ticket, ticket_in_db, ticket_expires)
        return self.validated 

    def validate_password(self, password):
        user = self.get_user_from_store()
        if user is None:
            self.password_valid = False
            return self.password_valid
        authid          = user.get("authid")
        stored_password = user.get("password")
        self.password_valid  = verify_password(password, stored_password)
        return self.password_valid

