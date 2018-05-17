import datetime
from app.lib.utils import generate_uuid, generate_verification_code, is_date_passed, get_future_date, get_now
from app.lib.crypt import decrypt


def test_generate_uuid_are_unique():
    a = generate_uuid()
    b = generate_uuid()
    assert a != b


def test_generate_verification_code_len_six():
    vc = generate_verification_code()
    assert len(str(vc)) == 6


def test_get_future_date():
    f = get_future_date(90)
    n = get_now()
    assert f > n 


def test_is_date_passed():
    is_passed = is_date_passed("2011-07-16T21:46:39Z")
    assert is_passed == True



