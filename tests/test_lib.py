from app.lib.utils import generate_uuid

def test_answer():
    a = generate_uuid()
    b = generate_uuid()
    assert a != b