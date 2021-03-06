import uuid
import datetime
import pytz
from dateutil import parser
from random import randint
from tempfile import NamedTemporaryFile
from types import MappingProxyType
import importlib.util
import os.path
import shutil
import sys

utc=pytz.UTC


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_now() -> datetime.datetime:
    return datetime.datetime.utcnow()


def get_future_date(seconds) -> datetime.datetime:
    return get_now() + datetime.timedelta(seconds=seconds)


def is_date_passed(date):
    return utc.localize(get_now()) > parser.parse(date)


def generate_verification_code() -> int:
    return randint(111111, 999999)


def get_file(path, extention) -> str:
    here_folder = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(here_folder, "../../" + path + "." + extention)
    return file_name


def parse_auth_header(auth_type, auth_header="") -> str:
    auth = auth_header.split()
    if len(auth) == 2 and auth[0] == auth_type:
        return auth[1]
    else:
        return None


def get_config(file_name) -> (str, str):
    try:
        config_dir = os.path.dirname(file_name)
        with NamedTemporaryFile(suffix='.py', dir=config_dir, delete=True) as tf:
            shutil.copyfile(file_name, tf.name)
            spec = importlib.util.spec_from_file_location('_config.settings', tf.name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        if hasattr(module, '__all__'):
            settings = {k: getattr(module, k) for k in module.__all__}
        else:
            settings = {k: v for k, v in vars(module).items() if not k.startswith('_')}

        return MappingProxyType(settings), None

    except Exception as e:
        sys.stderr.write('Failed to read config file: %s' % file_name)
        sys.stderr.flush()
        return None, e


def match_request(urls, method: str, path: str) -> bool:
    def match_item(item, path: str) -> bool:
        try:
            return bool(item.match(path))  # type: ignore
        except (AttributeError, TypeError):
            return item == path

    found = [item for item in urls if match_item(item, path)]
    if not found:
        return False

    if not isinstance(urls, dict):
        return True

    found_item = urls[found[0]]
    method = method.lower()
    if isinstance(found_item, str):
        return found_item.lower() == method

    return any(True for item in found_item if item.lower() == method)