from app.constants.errors import generate_error, error_dict

def test_generate_error():
    for error_type in error_dict:
        detail = "test"
        base_error = generate_error(error_type, detail=detail)
        error = base_error["error"]
        error_to_test = error_dict.get(error_type)
        assert error["code"] == error_to_test["code"]
        assert error["detail"] == detail
