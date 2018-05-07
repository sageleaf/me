import uuid
import datetime
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode

default_date_format = "%Y-%m-%d %H:%M:%S"
gmt_date_format = "%a, %d %b %Y %H:%M:%S GMT"

    
def generateUUID():
    return str(uuid.uuid4())


def generate_session_ticket():
    now = datetime.datetime.now()
    now_plus_10 = now + datetime.timedelta(minutes = 10)
    return {
        "ticket": generateUUID(),
        "expires": now_plus_10.strftime(default_date_format)
    }


def extend_ticket_life():
    now = datetime.datetime.now()
    now_plus_10 = now + datetime.timedelta(minutes = 10)
    return {
        "expires": now_plus_10.strftime(default_date_format)
    }


def validate_ticket(ticket, active_ticket, ticket_expires):
    match = ticket == active_ticket
    now = datetime.datetime.now().strftime(default_date_format)
    ticket_date = ticket_expires

    if not match or ( ticket_date < now ):
        return False
    return True


def verify_password(potential_pw, saved_pw):
    try :
        key = RSA.importKey(b64decode(PRIVATE_KEY))
        cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
        decrypted_saved_password = cipher.decrypt(b64decode(saved_pw))
        decrypted_potential_password = cipher.decrypt(b64decode(potential_pw))
        return decrypted_saved_password.decode('utf-8') == decrypted_potential_password.decode('utf-8')
    except:
        return False
