import logging.config
import os
import logging
import os.path as path
import json

module_path = os.path.dirname(__file__)
package_root = os.path.abspath(os.path.join(module_path, '..'))


if not path.exists("./logs"):
    os.mkdir("./logs")
    
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
      "simple": {
        "format": "%(levelname)s ==> %(module)s : %(message)s"
      },
      "detailed": {
        "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
        "datefmt": "%Y-%m-%dT%H:%M:%S%z"
      }
    },
    "handlers": {
      "stderr": {
        "class": "logging.StreamHandler",
        "level": "WARNING",
        "formatter": "simple",
        "stream": "ext://sys.stderr"
      },
      "file": {
        "class": "logging.handlers.RotatingFileHandler",
        "level": "DEBUG",
        "formatter": "detailed",
        "filename": "logs/goftino.log",
        "mode" : "+w",
        "maxBytes": 100000,
        "backupCount": 3
      }
    },
    "loggers": {
      "root": {
        "level": "DEBUG",
        "handlers": [
          "stderr",
          "file"
        ]
      }
    }
}

logging.config.dictConfig(logging_config)

