error_dict = {
    "general": {
        "code" : "SAGE-100",
        "type": "SERVER",
        "message" : "something unexpected happened"
    },
    "not_found": {
        "code" : "SAGE-404",
        "type": "CLIENT",
        "message" : "nothing found"
    },
    "need_more_info": {
        "code" : "SAGE-180",
        "type": "CLIENT",
        "message" : "you did not provide enough information to process your request"
    },
    "invalid_request": {
        "code" : "SAGE-6801",
        "type": "CLIENT",
        "message" : "request is malformed"
    },
    "invalid_login": {
        "code" : "SAGE-103",
        "type": "CLIENT",
        "message" : "invalid login credentials",
        "detail": "either you login or password is incorrect"
    },
    "invalid_application": {
        "code" : "SAGE-421",
        "type": "CLIENT",
        "message" : "invalid application",
        "detail": "please ensure that you are passing the correct api_key and app_id"
    },
    "jwt_error": {
        "code" : "SAGE-350",
        "type": "CLIENT",
        "message" : "invalid token"
    },
    "invalid_session": {
        "code" : "SAGE-325",
        "type": "CLIENT",
        "message" : "invalid session"
    },
    "invalid_header": {
        "code" : "SAGE-1016",
        "type": "CLIENT",
        "message" : "invalid header or manditory header missing"
    },
    "data_retrieval": {
        "code" : "SAGE-8402",
        "type": "SERVER",
        "message" : "error retrieving data from data source"
    },
    "data_persistance": {
        "code" : "SAGE-8401",
        "type": "SERVER",
        "message" : "error persisting data from data source"
    },
    "downstream_request": {
        "code" : "SAGE-8000",
        "type": "SERVER",
        "message" : "error retrieving data from data source"
    },
    "catastrophic": {
        "code" : "SAGE-8686",
        "type": "SERVER",
        "message" : "error retrieving data from data source"
    },
}


def generate_error(type='general', detail=None):
    base_error = { "error" : {}}
    type_error = error_dict.get(type)

    if detail is not None:
        type_error["detail"] = detail

    base_error["error"] = type_error

    return base_error

