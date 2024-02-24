import logging

import yaml

logger = logging.getLogger(__name__)


def read_config(config_path):
    with open(config_path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            logger.info("Pipeline Knowledge Building Config")
            return config
        except yaml.YAMLError:
            raise RuntimeError(
                f"Could not read config file. Possible parsing error in the config file: {config_path}"
            )
