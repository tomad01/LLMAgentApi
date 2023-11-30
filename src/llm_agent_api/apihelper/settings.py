import os
import logging
from dotenv import load_dotenv
from pathlib import Path

logger = logging.getLogger(__name__)


dotenv_path = Path(os.path.dirname(__file__)).parent / ".env"
load_dotenv(dotenv_path)


def env_test():
    some_test = os.environ.get("TEST_VAR")
    logger.info(f"var {some_test}")
