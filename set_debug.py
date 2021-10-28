import logging
import os

_LOGGER = logging.getLogger(__name__)

if os.path.isfile('test_bit') or os.environ.get("DEBUG", 0):
    os.environ["DEBUG"] = "1"
    _LOGGER.debug(f"Setting Debug env var to: {os.environ['DEBUG']}")
