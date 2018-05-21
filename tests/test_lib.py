import datetime
from app.lib.utils import generate_uuid, generate_verification_code, is_date_passed, get_future_date, get_now
from app.lib.tokens import encode_jwt_token, decode_jwt_token

# import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('test')


def test_encode_decode_jwt_token():
    t = encode_jwt_token("abc-123")
    d, e = decode_jwt_token(t)
    assert d == "abc-123"
    assert e == None


def test_encode_jwt_token_error():
    t = encode_jwt_token(bool)
    assert isinstance(t, TypeError)


def test_decode_jwt_token_error():
    d, e = decode_jwt_token("blah")
    assert d == None
    assert e == 'Invalid token. Please log in again.'


def test_decode_jwt_token_error():
    exp = datetime.datetime.utcnow() - datetime.timedelta(days=1, seconds=5)
    iat = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    t = encode_jwt_token(profile_id="blah", exp=exp, iat=iat )
    d, e = decode_jwt_token(t)
    assert d == None
    assert e == 'Signature expired. Please log in again.'


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



