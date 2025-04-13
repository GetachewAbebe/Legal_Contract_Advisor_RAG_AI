import logging
import os
import yaml
def setup_logger(name="contract_qna", config_path="config/logging.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    return logging.getLogger(name)
logger = setup_logger()