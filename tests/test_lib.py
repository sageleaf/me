from app.lib.utils import generate_uuid, generate_verification_code


def test_generate_uuid_are_unique():
    a = generate_uuid()
    b = generate_uuid()
    assert a != b


def test_generate_verification_code_len_six():
    vc = generate_verification_code()
    assert len(str(vc)) == 6
