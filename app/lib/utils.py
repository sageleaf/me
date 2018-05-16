import uuid
import datetime
import pytz
from dateutil import parser
from random import randint

utc=pytz.UTC

def generate_uuid():
    return str(uuid.uuid4())


def get_now():
    return datetime.datetime.utcnow()


def get_future_date(seconds):
    return get_now() + datetime.timedelta(seconds=seconds)


def is_date_passed(date):
    return utc.localize(get_now()) > parser.parse(date)


def generate_verification_code():
    return randint(111111, 999999)