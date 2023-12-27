"""
provides an influx client
"""
from os import getenv

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient  # type:ignore[import-untyped]

_INFLUX_USR_KEY = "INFLUX_USR"
_INFLUX_PWD_KEY = "INFLUX_PWD"
_INFLUX_ORG_KEY = "INFLUX_ORG"
_INFLUX_HOST_KEY = "INFLUX_HOST"


def create_influx_client_from_env_settings() -> InfluxDBClient:
    """
    creates an influx client from environment settings (.env or real env variables)
    :return: the influx client
    """
    load_dotenv()
    # see docker-compose.yml and .env.example for values (used e.g. in integration tests)
    influx_usr = getenv(_INFLUX_USR_KEY)
    influx_pwd = getenv(_INFLUX_PWD_KEY)
    influx_org = getenv(_INFLUX_ORG_KEY)
    influx_host = getenv(_INFLUX_HOST_KEY)  # e.g. "http://localhost:8086"
    if influx_usr is None:
        raise ValueError(f"Environment variable {_INFLUX_USR_KEY} is not set")
    if influx_pwd is None:
        raise ValueError(f"Environment variable {_INFLUX_PWD_KEY} is not set")
    if influx_org is None:
        raise ValueError(f"Environment variable {_INFLUX_ORG_KEY} is not set")
    if not influx_host:
        raise ValueError(f"Environment variable {_INFLUX_HOST_KEY} is not set")
    client = InfluxDBClient(url=influx_host, username=influx_usr, password=influx_pwd, org=influx_org)
    readiness = client.ready()
    if readiness.status != "ready":
        raise ConnectionError(f"Connected to InfluxDB @{influx_host} but client is not ready")
    return client