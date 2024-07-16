# Standard Library
import logging
from logging.config import dictConfig

import environ

dictConfig(
    config={
        "version": 1,
        "formatters": {
            "f": {
                "format": '{"level": "%(levelname)-4s", "timestamp": "%(asctime)s",'  # noqa
                          '"module": "%(name)s", "body": "%(message)s"}'
            }
        },
        "handlers": {
            "h": {
                "class": "logging.StreamHandler",
                "formatter": "f",
                "level": logging.INFO,
            }
        },
        "root": {
            "handlers": ["h"],
            "level": logging.INFO,
        },
    }
)


@environ.config(prefix="")
class AppConfig:
    @environ.config(prefix="API")
    class API:
        host = environ.var()
        title = environ.var()
        version = environ.var()
        prefix = environ.var()
        debug = environ.bool_var()
        allowed_hosts = environ.var()

    @environ.config(prefix="MONGO")
    class Mongo:
        host = environ.var()
        port = environ.var(converter=int)
        username = environ.var()
        password = environ.var()
        db = environ.var()

    env = environ.var()

    api: API = environ.group(API)
    mongo: Mongo = environ.group(Mongo)
    translate_service_url = environ.var()


CONFIG: AppConfig = AppConfig.from_environ()  # type: ignore
