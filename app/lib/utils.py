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


def get_file(path, extention):
    here_folder = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(here_folder, "../../" + path + "." + extention)
    return file_name


def get_config(file_name):
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

        return MappingProxyType(settings)

    except Exception:
        sys.stderr.write('Failed to read config file: %s' % file_name)
        sys.stderr.flush()
        raise