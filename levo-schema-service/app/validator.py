from openapi_spec_validator import validate_spec
import yaml, json
from typing import Tuple

def load_spec_bytes(bytestr: bytes):
    try:
        return json.loads(bytestr.decode())
    except:
        pass
    try:
        return yaml.safe_load(bytestr.decode())
    except:
        raise ValueError("Unable to parse spec as JSON or YAML")

def validate_openapi(bytestr: bytes) -> Tuple[bool, str]:
    try:
        spec = load_spec_bytes(bytestr)
        validate_spec(spec)
        return True, "OK"
    except Exception as e:
        return False, str(e)
